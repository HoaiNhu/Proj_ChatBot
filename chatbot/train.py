from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
import torch
import json
import os

# Load dữ liệu chính
with open('data.json', encoding='utf-8') as f:
    data = json.load(f)

# Load từ viết tắt
abbreviations = {}
with open('abbreviations.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if ' = ' in line:
            abbr, full = line.split(' = ', 1)
            abbreviations[abbr.strip()] = full.strip()
        else:
            print(f"⚠️ Bỏ qua dòng không hợp lệ: {line}")


# Sinh dữ liệu mới từ từ viết tắt
expanded_data = []
for item in data:
    text = item['text']
    intent = item['intent']
    expanded_data.append({"text": text, "intent": intent})  # Giữ nguyên câu gốc
    # Thay thế từ đầy đủ bằng từ viết tắt
    for abbr, full in abbreviations.items():
        if full in text:
            new_text = text.replace(full, abbr)
            expanded_data.append({"text": new_text, "intent": intent})

# Chuẩn bị dataset
texts = [item['text'] for item in expanded_data]
labels = [0 if item['intent'] == 'suggest_cake' else 1 if item['intent'] == 'ask_price' else 2 for item in expanded_data]
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
encodings = tokenizer(texts, truncation=True, padding=True)

class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item
    def __len__(self):
        return len(self.labels)

dataset = Dataset(encodings, labels)
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=3)

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

trainer.train()
model.save_pretrained('trained_model')
tokenizer.save_pretrained('trained_model')

from pymongo import MongoClient

mongo_uri = os.getenv('MONGO_URI', 'mongodb+srv://hnhu:hoainhu1234@webbuycake.asd8v.mongodb.net/?retryWrites=true&w=majority&appName=WebBuyCake')
client = MongoClient(mongo_uri)
db = client['test']
chats = db['chats']

# Lấy dữ liệu từ MongoDB
mongo_data = []
for chat in chats.find():
    user_input = chat['user']
    bot_response = chat['bot']
    if "Bạn thích bánh vị gì?" in bot_response:
        intent = "suggest_cake"
    elif "giá" in bot_response:
        intent = "ask_price"
    elif "kết nối" in bot_response:
        intent = "connect_staff"
    else:
        continue
    mongo_data.append({"text": user_input, "intent": intent})

# Kết hợp với data.json
with open('data.json', encoding='utf-8') as f:
    data = json.load(f)

expanded_data = data + mongo_data