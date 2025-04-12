import torch
from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import re
import os
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()

# Kết nối MongoDB Atlas
try:
    mongo_uri = os.getenv('MONGO_URI', 'mongodb+srv://hnhu:hoainhu1234@webbuycake.asd8v.mongodb.net/?retryWrites=true&w=majority&appName=WebBuyCake')
    client = MongoClient(mongo_uri)
    db = client['test']
    chats = db['chats']
    print("Connected to MongoDB Atlas")
except Exception as e:
    print(f"Failed to connect to MongoDB Atlas: {e}")
    exit(1)

# Đọc từ viết tắt
abbreviations = {}
try:
    with open('abbreviations.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or '=' not in line:
                continue
            abbr, full = line.strip().split(' = ')
            abbreviations[abbr] = full
except FileNotFoundError:
    print("Error: abbreviations.txt not found")
    exit(1)

# Hàm xử lý từ viết tắt
def replace_abbreviations(text):
    for abbr, full in sorted(abbreviations.items(), key=lambda x: len(x[0]), reverse=True):
        text = re.sub(r'\b' + re.escape(abbr) + r'\b', full, text)
    return text

# Tải mô hình và tokenizer
try:
    if not os.path.exists('trained_model'):
        raise FileNotFoundError("trained_model directory not found")
    tokenizer = DistilBertTokenizer.from_pretrained('trained_model')
    model = DistilBertForSequenceClassification.from_pretrained('trained_model')
    print("Loaded trained_model")
except Exception as e:
    print(f"Error loading trained_model: {e}")
    print("Falling back to distilbert-base-uncased")
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=3)

# Dự đoán intent
def predict_intent(user_input):
    user_input = replace_abbreviations(user_input)
    inputs = tokenizer(user_input, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    return predicted_class

# Truy vấn thông tin sản phẩm từ MongoDB
def get_product_info(product_name):
    if not isinstance(product_name, str):
        return None
    
    try:
        product = db['products'].find_one({"productName": {"$regex": re.escape(product_name), "$options": "i"}})
    except Exception as e:
        print(f"Error querying MongoDB: {e}")
        return None
    
    if product:
        print (product_name)
        return product
    else:
        return None

# Cập nhật hàm get_response() để sử dụng thông tin sản phẩm từ MongoDB
def get_response(user_input):
    intent = predict_intent(user_input)
    
    if intent == 0:  # suggest_cake
        response = "Bạn thích vị gì nè? Socola, vani, hay trà xanh? Mình gợi ý thêm nhé!"
    elif intent == 1:  # ask_price
        product_name = extract_product_name(user_input)
        product_info = get_product_info(product_name)
        print ("San pham ", product_info)
        if product_info:
            response = f"Sản phẩm {product_info['productName']} có giá {product_info['productPrice']} VND.\nMô tả {product_info['productDescription']}"
        else:
            response = "Mình không tìm thấy sản phẩm này. Bạn có thể thử lại với tên khác hoặc chọn một sản phẩm từ danh sách của chúng mình?"
    elif intent == 2:  # connect_staff
        response = "Oke, để mình kết nối bạn với nhân viên nha. Chờ xíu nè!"
    else:
        response = "Hihi, mình chưa hiểu lắm. Bạn nhắn lại rõ hơn nha!"
    
    try:
        chats.insert_one({'user': user_input, 'bot': response, 'timestamp': datetime.now()})
    except Exception as e:
        print(f"Error saving to MongoDB: {e}")
    
    return response

# Tạo hàm extract_product_name()
def extract_product_name(user_input):
    try:
        # Lấy tất cả tên sản phẩm từ MongoDB
        product_docs = db['products'].find({}, {'productName': 1, '_id': 0})
        product_names = [doc['productName'] for doc in product_docs]
    except Exception as e:
        print(f"Error fetching product names: {e}")
        return None

    # Kiểm tra xem user_input có khớp với product name nào không
    for product in product_names:
        if re.search(r'\b' + re.escape(product) + r'\b', user_input, re.IGNORECASE):
            return product
    
    return None


# API Flask
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message', '')
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400
        response = get_response(user_input)
        return jsonify({'text': response})
    except Exception as e:
        print(f"Error in /chat: {e}")
        return jsonify({'error': 'Invalid request'}), 400

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        if 'message' in data:  # Zalo format
            user_input = data['message']['text']
        else:  # Facebook format
            user_input = data['entry'][0]['messaging'][0]['message']['text']
        response = get_response(user_input)
        return jsonify({'status': 'success'})
    except KeyError:
        print("Error: Invalid webhook format")
        return jsonify({'error': 'Invalid webhook format'}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005, debug=True)
