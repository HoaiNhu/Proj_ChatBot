from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
import torch
import json
import os
from config.config_chatbot import ChatbotConfig
from utils.logger import logger
from pymongo import MongoClient
from logic.intent_list import INTENT_LIST
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# Load dữ liệu chính
with open('data/data.json', encoding='utf-8') as f:
    data = json.load(f)

# Load dữ liệu học tập từ learning_system
if os.path.exists('learning_data.json'):
    with open('learning_data.json', encoding='utf-8') as f:
        learning_data = json.load(f)
else: 
    learning_data = []

# Load từ viết tắt
abbreviations = {}
with open('data/abbreviations.txt', 'r', encoding='utf-8') as f:
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
mongo_uri = ChatbotConfig.CHATBOT_MONGO_URI
client = MongoClient(mongo_uri)
db = client[ChatbotConfig.CHATBOT_DB_NAME]
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
    INTENT_LIST.index(item['intent']) if item['intent'] in INTENT_LIST else -1
    for item in expanded_data
]
# Loại bỏ các mẫu không có intent hợp lệ
valid_data = [(t, l) for t, l in zip(texts, labels) if l != -1]
texts, labels = zip(*valid_data) if valid_data else ([], [])

tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
encodings = tokenizer(texts, truncation=True, padding=True, max_length=ChatbotConfig.MAX_LENGTH)

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
model = DistilBertForSequenceClassification.from_pretrained(
    'distilbert-base-uncased',
    num_labels=len(INTENT_LIST)
)

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=ChatbotConfig.TRAINING_EPOCHS,
    per_device_train_batch_size=ChatbotConfig.BATCH_SIZE,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    learning_rate=ChatbotConfig.LEARNING_RATE
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

# Sau khi train xong, đánh giá trên tập train/test (nếu có)
def evaluate_model(trainer, dataset, labels_true):
    preds_output = trainer.predict(dataset)
    preds = np.argmax(preds_output.predictions, axis=1)
    report = classification_report(labels_true, preds, target_names=INTENT_LIST)
    matrix = confusion_matrix(labels_true, preds)
    print("Classification Report:")
    print(report)
    print("Confusion Matrix:")
    print(matrix)
    # Log ra file
    logger.info("Classification Report:\n" + report)
    logger.info("Confusion Matrix:\n" + np.array2string(matrix))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "eval":
        # Đánh giá lại model đã train (không train lại)
        model = DistilBertForSequenceClassification.from_pretrained(ChatbotConfig.MODEL_PATH)
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=dataset,
        )
        evaluate_model(trainer, dataset, labels)
    else:
        # Train và đánh giá như cũ
        trainer.train()
        model.save_pretrained(ChatbotConfig.MODEL_PATH)
        tokenizer.save_pretrained(ChatbotConfig.MODEL_PATH)
        logger.info("Model training completed and saved")
        evaluate_model(trainer, dataset, labels)