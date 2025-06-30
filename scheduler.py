import schedule
import time
import subprocess
from datetime import datetime, timedelta
from pymongo import MongoClient
from config.config_chatbot import ChatbotConfig
from utils.logger import logger

def retrain_model():
    logger.info("Retraining model...")
    subprocess.run(["python", "train.py"])
    logger.info("Model retrained successfully")

def release_escalated_sessions(timeout_minutes=10):
    try:
        client = MongoClient(ChatbotConfig.CHATBOT_MONGO_URI)
        db = client[ChatbotConfig.CHATBOT_DB_NAME]
        now = datetime.now()
        timeout_time = now - timedelta(minutes=timeout_minutes)
        result = db["conversations"].update_many(
            {"status": "escalated", "updatedAt": {"$lt": timeout_time}},
            {"$set": {"status": "active"}}
        )
        if result.modified_count > 0:
            logger.info(f"Đã trả lại quyền trả lời cho bot ở {result.modified_count} session.")
    except Exception as e:
        logger.error(f"Lỗi khi kiểm tra escalated sessions: {e}")

# Lên lịch retrain model mỗi ngày lúc 02:00 (nếu cần)
schedule.every().day.at("02:00").do(retrain_model)
# Lên lịch kiểm tra escalated sessions mỗi phút
schedule.every(1).minutes.do(release_escalated_sessions)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(10)

if __name__ == "__main__":
    logger.info("Starting scheduler...")
    run_scheduler()