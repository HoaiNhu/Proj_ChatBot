from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
import torch
import json
import os
from config.config_chatbot import ChatbotConfig
from pymongo import MongoClient
from logic.intent_list import INTENT_LIST
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import numpy as np
from utils.logger import logger

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

# Lấy data training từ nhiều collection của cửa hàng
store_client = MongoClient(ChatbotConfig.STORE_MONGO_URI)
store_db = store_client[ChatbotConfig.STORE_DB_NAME]

def extract_training_samples():
    samples = []
    # Products
    for prod in store_db['products'].find():
        if 'productName' in prod:
            samples.append({"text": f"Bánh {prod['productName']} có ngon không?", "intent": "suggest_cake"})
        if 'productDescription' in prod:
            samples.append({"text": prod['productDescription'], "intent": "suggest_cake"})
    # Orders
    for order in store_db['orders'].find():
        if 'orderCode' in order:
            samples.append({"text": f"Đơn hàng mã {order['orderCode']} đã giao chưa?", "intent": "check_order"})
    # News
    for news in store_db['news'].find():
        if 'newsTitle' in news:
            samples.append({"text": news['newsTitle'], "intent": "ask_promotion"})
        if 'newsContent' in news:
            samples.append({"text": news['newsContent'], "intent": "ask_promotion"})
    # Discounts
    for discount in store_db['discounts'].find():
        if 'discountName' in discount:
            samples.append({"text": discount['discountName'], "intent": "ask_promotion"})
    # Categories
    for cat in store_db['categories'].find():
        if 'categoryName' in cat:
            samples.append({"text": f"Shop có bánh {cat['categoryName']} không?", "intent": "suggest_cake"})
    # Ratings
    for rating in store_db['ratings'].find():
        if 'comment' in rating:
            samples.append({"text": rating['comment'], "intent": "ask_feedback"})
    return samples

# Thêm data từ các collection trên vào expanded_data
expanded_data.extend(extract_training_samples())

# Chuẩn bị dataset
texts = [item['text'] for item in expanded_data]
labels = [
    INTENT_LIST.index(item['intent']) if item['intent'] in INTENT_LIST else -1
    for item in expanded_data
]
# Loại bỏ các mẫu không có intent hợp lệ
valid_data = [(t, l) for t, l in zip(texts, labels) if l != -1]
texts, labels = zip(*valid_data) if valid_data else ([], [])

# Tách tập train/validation (80% train, 20% val)
texts_train, texts_val, labels_train, labels_val = train_test_split(
    texts, labels, test_size=0.2, random_state=42, stratify=labels
)

tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
encodings_train = tokenizer(list(texts_train), truncation=True, padding=True, max_length=ChatbotConfig.MAX_LENGTH)
encodings_val = tokenizer(list(texts_val), truncation=True, padding=True, max_length=ChatbotConfig.MAX_LENGTH)

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

train_dataset = Dataset(encodings_train, list(labels_train))
val_dataset = Dataset(encodings_val, list(labels_val))
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
    train_dataset=train_dataset,
)

# Sau khi train xong, đánh giá trên tập train/test (nếu có)
def evaluate_model(trainer, dataset, labels_true, report_file="eval_report.txt"):
    preds_output = trainer.predict(dataset)
    preds = np.argmax(preds_output.predictions, axis=1)
    unique_labels = sorted(set(labels_true) | set(preds))
    report = classification_report(
        labels_true,
        preds,
        labels=unique_labels,
        target_names=[INTENT_LIST[i] for i in unique_labels],
        zero_division=0
    )
    matrix = confusion_matrix(labels_true, preds, labels=unique_labels)
    print("Classification Report:")
    print(report)
    print("Confusion Matrix:")
    print(matrix)
    # Log ra file
    logger.info("Classification Report:\n" + report)
    logger.info("Confusion Matrix:\n" + np.array2string(matrix))
    # Lưu ra file txt
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("Classification Report:\n")
        f.write(report)
        f.write("\nConfusion Matrix:\n")
        f.write(np.array2string(matrix))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "eval":
        # Đánh giá lại model đã train (không train lại)
        model = DistilBertForSequenceClassification.from_pretrained(ChatbotConfig.MODEL_PATH)
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
        )
        evaluate_model(trainer, val_dataset, labels_val)
    else:
        # Train và đánh giá như cũ
        trainer.train()
        model.save_pretrained(ChatbotConfig.MODEL_PATH)
        tokenizer.save_pretrained(ChatbotConfig.MODEL_PATH)
        logger.info("Model training completed and saved")
        evaluate_model(trainer, val_dataset, labels_val)