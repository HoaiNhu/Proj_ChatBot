import torch
from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import re
import os
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
import uuid

# Import các module mới
from config import Config
from logger import logger
from learning_system import LearningSystem
from messenger_integration import MessengerIntegration

# Load biến môi trường
load_dotenv()

# Kết nối MongoDB Atlas
try:
    client = MongoClient(Config.MONGO_URI)
    db = client['test']
    chats = db['chats']
    logger.info("Connected to MongoDB Atlas")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB Atlas: {e}")
    exit(1)

# Khởi tạo các hệ thống
learning_system = LearningSystem(db)
messenger_integration = MessengerIntegration()

# Đọc từ viết tắt
abbreviations = {}
try:
    with open('abbreviations.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or '=' not in line:
                continue
            abbr, full = line.strip().split(' = ')
            abbreviations[abbr] = full
    logger.info("Loaded abbreviations successfully")
except FileNotFoundError:
    logger.error("Error: abbreviations.txt not found")
    exit(1)

# Hàm xử lý từ viết tắt
def replace_abbreviations(text):
    for abbr, full in sorted(abbreviations.items(), key=lambda x: len(x[0]), reverse=True):
        text = re.sub(r'\b' + re.escape(abbr) + r'\b', full, text)
    return text

# Tải mô hình và tokenizer
try:
    if not os.path.exists(Config.MODEL_PATH):
        raise FileNotFoundError(f"{Config.MODEL_PATH} directory not found")
    tokenizer = DistilBertTokenizer.from_pretrained(Config.MODEL_PATH)
    model = DistilBertForSequenceClassification.from_pretrained(Config.MODEL_PATH)
    logger.info("Loaded trained model successfully")
except Exception as e:
    logger.warning(f"Error loading trained model: {e}")
    logger.info("Falling back to distilbert-base-uncased")
    tokenizer = DistilBertTokenizer.from_pretrained(Config.FALLBACK_MODEL)
    model = DistilBertForSequenceClassification.from_pretrained(Config.FALLBACK_MODEL, num_labels=6)  # Cập nhật num_labels cho ý định mới

# Dự đoán intent với confidence score
def predict_intent(user_input):
    user_input = replace_abbreviations(user_input)
    inputs = tokenizer(user_input, return_tensors="pt", truncation=True, padding=True, max_length=Config.MAX_LENGTH)
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    predicted_class = torch.argmax(logits, dim=1).item()
    confidence = probabilities[0][predicted_class].item()
    
    logger.info(f"Intent prediction: {predicted_class} with confidence: {confidence:.3f}")
    return predicted_class, confidence

# Truy vấn thông tin sản phẩm từ MongoDB
def get_product_info(product_name):
    if not isinstance(product_name, str):
        return None
    
    try:
        product = db['products'].find_one({"productName": {"$regex": re.escape(product_name), "$options": "i"}})
    except Exception as e:
        logger.error(f"Error querying MongoDB: {e}")
        return None
    
    if product:
        logger.info(f"Found product: {product_name}")
        return product
    else:
        logger.info(f"Product not found: {product_name}")
        return None

# Gợi ý sản phẩm dựa trên sở thích
def suggest_products(user_input):
    keywords = ['socola', 'vani', 'trà xanh', 'trái cây', 'tiramisu', 'mousse', 'red velvet', 'matcha']
    matched_keywords = [kw for kw in keywords if kw.lower() in user_input.lower()]
    
    try:
        if not matched_keywords:
            products = db['products'].find({'isPopular': True}).limit(3)
        else:
            products = db['products'].find({
                '$or': [
                    {'productDescription': {'$regex': kw, '$options': 'i'}} for kw in matched_keywords
                ]
            }).limit(3)
        return list(products)
    except Exception as e:
        logger.error(f"Error suggesting products: {e}")
        return []

# Trích xuất tên sản phẩm với fuzzy matching
def extract_product_name(user_input):
    try:
        product_docs = db['products'].find({}, {'productName': 1, '_id': 0})
        product_names = [doc['productName'] for doc in product_docs]
    except Exception as e:
        logger.error(f"Error fetching product names: {e}")
        return None

    best_match = None
    best_score = 0
    for product in product_names:
        score = fuzz.token_sort_ratio(product.lower(), user_input.lower())
        if score > 80 and score > best_score:
            best_match = product
            best_score = score
    
    return best_match

# Cập nhật hàm get_response() để sử dụng ngữ cảnh và ý định mới
def get_response(user_input, platform='web', user_id=None, session_id=None):
    intent, confidence = predict_intent(user_input)
    
    # Kiểm tra ngữ cảnh từ tin nhắn trước
    if session_id:
        last_chat = chats.find_one({'sessionId': session_id}, sort=[('timestamp', -1)])
        last_product = last_chat.get('context', {}).get('last_product') if last_chat else None
    else:
        last_product = None
    
    product_name = extract_product_name(user_input) or last_product
    
    # Thu thập dữ liệu cuộc trò chuyện
    learning_system.collect_conversation_data(user_input, "", intent, confidence)
    
    if intent == 0:  # suggest_cake
        products = suggest_products(user_input)
        if products:
            response = "Mình gợi ý vài loại bánh nè:\n" + "\n".join(
                [f"- {p['productName']}: {p['productDescription']} (Giá: {p['productPrice']} VND)"
                 for p in products]
            )
        else:
            response = "Bạn thích vị gì nè? Socola, vani, hay trà xanh? Mình gợi ý thêm nhé!"
    elif intent == 1:  # ask_price
        product_info = get_product_info(product_name) if product_name else None
        if product_info:
            response = f"Sản phẩm {product_info['productName']} có giá {product_info['productPrice']} VND.\nMô tả: {product_info['productDescription']}"
        else:
            response = "Mình không tìm thấy sản phẩm này. Bạn có thể thử lại với tên khác hoặc chọn một sản phẩm từ danh sách của chúng mình?"
    elif intent == 2:  # connect_staff
        response = "Oke, để mình kết nối bạn với nhân viên nha. Chờ xíu nè!"
    elif intent == 3:  # ask_promotion
        promotions = db['promotions'].find().limit(3)
        if promotions:
            response = "Hiện tại shop có các khuyến mãi sau:\n" + "\n".join(
                [f"- {p['name']}: {p['description']}" for p in promotions]
            )
        else:
            response = "Hiện tại chưa có khuyến mãi nào, bạn theo dõi shop để cập nhật nha!"
    elif intent == 4:  # check_order
        response = "Vui lòng cung cấp mã đơn hàng để mình kiểm tra nha!"
    elif intent == 5:  # custom_cake
        response = "Bạn muốn bánh tùy chỉnh thế nào? Gửi mình ý tưởng hoặc hình ảnh nha, mình sẽ chuyển cho đội ngũ thiết kế!"
    else:
        response = "Hihi, mình chưa hiểu lắm. Bạn nhắn lại rõ hơn nha!"
    
    # Cập nhật response trong learning system
    learning_system.collect_conversation_data(user_input, response, intent, confidence)
    
    # Gửi tin nhắn qua platform nếu cần
    if platform in ['facebook', 'zalo'] and user_id:
        messenger_integration.send_message(platform, user_id, response)
    
    try:
        chats.insert_one({
            'user': user_input,
            'bot': response,
            'intent': intent,
            'confidence': confidence,
            'platform': platform,
            'user_id': user_id,
            'sessionId': session_id or str(uuid.uuid4()),
            'context': {'last_product': product_name} if product_name else {},
            'timestamp': datetime.now()
        })
    except Exception as e:
        logger.error(f"Error saving to MongoDB: {e}")
    
    return response, session_id or str(uuid.uuid4())

# API Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

def check_api_key():
    api_key = request.headers.get('X-API-Key')
    if api_key != Config.API_KEY:
        return jsonify({'error': 'Invalid API key'}), 401
    return None

@app.route('/chat', methods=['POST'])
def chat():
    try:
        auth_error = check_api_key()
        if auth_error:
            return auth_error
        data = request.json
        user_input = data.get('message', '')
        session_id = data.get('sessionId')
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400
        
        response, session_id = get_response(user_input, session_id=session_id)
        return jsonify({'text': response, 'sessionId': session_id})
    except Exception as e:
        logger.error(f"Error in /chat: {e}")
        return jsonify({'error': 'Invalid request'}), 400

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Xử lý Facebook webhook
        facebook_result = messenger_integration.handle_facebook_webhook()
        if facebook_result:
            if isinstance(facebook_result, str):
                return facebook_result
            elif isinstance(facebook_result, dict):
                response, session_id = get_response(
                    facebook_result['message'],
                    facebook_result['platform'],
                    facebook_result['user_id'],
                    facebook_result.get('sessionId')
                )
                return jsonify({'status': 'success', 'sessionId': session_id})
        
        # Xử lý Zalo webhook
        zalo_result = messenger_integration.handle_zalo_webhook()
        if zalo_result:
            if isinstance(zalo_result, dict) and 'platform' in zalo_result:
                response, session_id = get_response(
                    zalo_result['message'],
                    zalo_result['platform'],
                    zalo_result['user_id'],
                    zalo_result.get('sessionId')
                )
                return jsonify({'status': 'success', 'sessionId': session_id})
            else:
                return zalo_result
        
        # Fallback cho format cũ
        data = request.json
        if 'message' in data:  # Zalo format
            user_input = data['message']['text']
            user_id = data['sender']['id']
            session_id = data.get('sessionId')
        else:  # Facebook format
            user_input = data['entry'][0]['messaging'][0]['message']['text']
            user_id = data['entry'][0]['messaging'][0]['sender']['id']
            session_id = data.get('sessionId')
        
        response, session_id = get_response(user_input, 'facebook' if 'entry' in data else 'zalo', user_id, session_id)
        return jsonify({'status': 'success', 'sessionId': session_id})
        
    except Exception as e:
        logger.error(f"Error in /webhook: {e}")
        return jsonify({'error': 'Invalid webhook format'}), 400

@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        data = request.json
        user_input = data.get('user_input', '')
        bot_response = data.get('bot_response', '')
        is_helpful = data.get('is_helpful', False)
        feedback_text = data.get('feedback_text', '')
        
        learning_system.collect_feedback(user_input, bot_response, is_helpful, feedback_text)
        
        return jsonify({'status': 'success'})
    except Exception as e:
        logger.error(f"Error in /feedback: {e}")
        return jsonify({'error': 'Invalid feedback data'}), 400

@app.route('/metrics', methods=['GET'])
def get_metrics():
    try:
        days_back = request.args.get('days', 30, type=int)
        metrics = learning_system.get_performance_metrics(days_back)
        return jsonify(metrics)
    except Exception as e:
        logger.error(f"Error in /metrics: {e}")
        return jsonify({'error': 'Failed to get metrics'}), 500

@app.route('/retrain', methods=['POST'])
def retrain_model():
    try:
        auth_error = check_api_key()
        if auth_error:
            return auth_error
        
        new_data = learning_system.analyze_conversations()
        if new_data:
            os.system('python train.py')
            logger.info("Model retraining completed")
            return jsonify({'status': 'success', 'new_samples': len(new_data)})
        else:
            return jsonify({'status': 'no_new_data'})
    except Exception as e:
        logger.error(f"Error in /retrain: {e}")
        return jsonify({'error': 'Failed to retrain model'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    try:
        db.command('ping')
        test_input = "test"
        predict_intent(test_input)
        
        return jsonify({
            'status': 'healthy',
            'mongodb': 'connected',
            'model': 'loaded',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == "__main__":
    logger.info("Starting chatbot server...")
    app.run(host='0.0.0.0', port=5005, debug=Config.DEBUG)