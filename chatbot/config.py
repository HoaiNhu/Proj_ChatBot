import os
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()

class Config:
    # MongoDB Configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://hnhu:hoainhu1234@webbuycake.asd8v.mongodb.net/?retryWrites=true&w=majority&appName=WebBuyCake')
    
    # Facebook Messenger Configuration
    FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN', '')
    FACEBOOK_VERIFY_TOKEN = os.getenv('FACEBOOK_VERIFY_TOKEN', '')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'chatbot.log')
    
    # Model Configuration
    MODEL_PATH = 'trained_model'
    FALLBACK_MODEL = 'distilbert-base-uncased'
    MAX_LENGTH = 512
    
    # Training Configuration
    TRAINING_EPOCHS = 3
    BATCH_SIZE = 8
    LEARNING_RATE = 2e-5 