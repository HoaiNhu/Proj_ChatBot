import schedule
import time
import subprocess
from logger import logger

def retrain_model():
    logger.info("Retraining model...")
    subprocess.run(["python", "train.py"])
    logger.info("Model retrained successfully")

schedule.every().day.at("02:00").do(retrain_model)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    logger.info("Starting scheduler...")
    run_scheduler()