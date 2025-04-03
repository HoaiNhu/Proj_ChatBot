from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

# Kết nối MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['avocado']
chats = db['chats']

# Tải mô hình và tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=3)  # 3 intents

# Dự đoán intent
def predict_intent(user_input):
    inputs = tokenizer(user_input, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    return predicted_class

# Logic Programming để trả lời
def get_response(user_input):
    intent = predict_intent(user_input)
    if intent == 0:  # suggest_cake
        response = "Bạn thích bánh vị gì? Socola, vani hay trái cây?"
    elif intent == 1:  # ask_price
        response = "Bánh Chocolate Lava giá 250.000 VNĐ, Black Forest giá 300.000 VNĐ."
    elif intent == 2:  # connect_staff
        response = "Tôi sẽ kết nối bạn với nhân viên. Vui lòng đợi chút nhé!"
    else:
        response = "Xin lỗi, tôi chưa hiểu. Bạn có thể nói rõ hơn không?"
    
    # Lưu vào MongoDB để tự học hỏi
    chats.insert_one({'user': user_input, 'bot': response, 'timestamp': datetime.now()})
    return response

# API Flask
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    response = get_response(user_input)
    return jsonify({'text': response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005)

#Integrate social
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    user_input = data['entry'][0]['messaging'][0]['message']['text']  # Facebook Messenger format
    response = get_response(user_input)
    # Gửi lại qua API của Messenger/Zalo/Telegram
    return jsonify({'status': 'success'})