from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
import torch
import json
import os
from config.config_chatbot import Config
from utils.logger import logger
from pymongo import MongoClient

# Load dữ liệu chính
with open('data.json', encoding='utf-8') as f:
    data = json.load(f)

# Load dữ liệu học tập từ learning_system
if os.path.exists('learning_data.json'):
    with open('learning_data.json', encoding='utf-8') as f:
        learning_data = json.load(f)
else:
    learning_data = []

# Load từ viết tắt
abbreviations = {}
with open('abbreviations.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if ' = ' in line:
            abbr, full = line.split(' = ', 1)
            abbreviations[abbr.strip()] = full.strip()
        else:
            logger.warning(f"Bỏ qua dòng không hợp lệ: {line}")

# Sinh dữ liệu mới từ từ viết tắt
expanded_data = []
for item in data + learning_data:
    text = item['text']
    intent = item['intent']
    expanded_data.append({"text": text, "intent": intent})
    for abbr, full in abbreviations.items():
        if full in text:
            new_text = text.replace(full, abbr)
            expanded_data.append({"text": new_text, "intent": intent})

# Lấy dữ liệu từ MongoDB
mongo_uri = Config.MONGO_URI
client = MongoClient(mongo_uri)
db = client['test']
chats = db['chats']

mongo_data = []
for chat in chats.find():
    user_input = chat['user']
    intent = chat.get('intent')
    if intent:
        mongo_data.append({"text": user_input, "intent": intent})

# Kết hợp dữ liệu
expanded_data.extend(mongo_data)

# Chuẩn bị dataset
texts = [item['text'] for item in expanded_data]
labels = [
    0 if item['intent'] == 'suggest_cake' else
    1 if item['intent'] == 'ask_price' else
    2 if item['intent'] == 'connect_staff' else
    3 if item['intent'] == 'ask_promotion' else
    4 if item['intent'] == 'check_order' else
    5 if item['intent'] == 'custom_cake' else -1
    for item in expanded_data
]
# Loại bỏ các mẫu không có intent hợp lệ
valid_data = [(t, l) for t, l in zip(texts, labels) if l != -1]
texts, labels = zip(*valid_data) if valid_data else ([], [])

tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
encodings = tokenizer(texts, truncation=True, padding=True, max_length=Config.MAX_LENGTH)

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
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=6)

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=Config.TRAINING_EPOCHS,
    per_device_train_batch_size=Config.BATCH_SIZE,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    learning_rate=Config.LEARNING_RATE
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

trainer.train()
model.save_pretrained(Config.MODEL_PATH)
tokenizer.save_pretrained(Config.MODEL_PATH)
logger.info("Model training completed and saved")