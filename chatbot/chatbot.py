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

# Logic trả lời
def get_response(user_input):
    intent = predict_intent(user_input)
    if intent == 0:  # suggest_cake
        response = "Bạn thích vị gì nè? Socola, vani, hay trà xanh? Mình gợi ý thêm nhé!"
    elif intent == 1:  # ask_price
        response = "Bánh Chocolate Lava 250k, Black Forest 300k. Bạn muốn hỏi loại nào nữa ko?"
    elif intent == 2:  # connect_staff
        response = "Oke, để mình kết nối bạn với nhân viên nha. Chờ xíu nè!"
    else:
        response = "Hihi, mình chưa hiểu lắm. Bạn nhắn lại rõ hơn nha!"
    
    # Lưu vào MongoDB Atlas
    try:
        chats.insert_one({'user': user_input, 'bot': response, 'timestamp': datetime.now()})
    except Exception as e:
        print(f"Error saving to MongoDB: {e}")
    return response

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
        # TODO: Implement sending response via Messenger/Zalo API
        return jsonify({'status': 'success'})
    except KeyError:
        print("Error: Invalid webhook format")
        return jsonify({'error': 'Invalid webhook format'}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005, debug=True)