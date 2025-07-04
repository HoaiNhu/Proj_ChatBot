import os
from dotenv import load_dotenv

load_dotenv()

class ChatbotConfig:
    """Cấu hình riêng cho chatbot và cửa hàng"""
    
    # MongoDB cho cửa hàng (data training)
    STORE_MONGO_URI = os.getenv("STORE_MONGO_URI", "mongodb+srv://hnhu:hoainhu1234@webbuycake.asd8v.mongodb.net/?retryWrites=true&w=majority&appName=WebBuyCake")
    STORE_DB_NAME = os.getenv("STORE_DB_NAME", "test")

    # MongoDB cho chatbot (conversation, feedback, ...)
    CHATBOT_MONGO_URI = os.getenv("CHATBOT_MONGO_URI", "mongodb+srv://hnhu1234:hoainhu1234@cluster0.xnyrq6o.mongodb.net/")
    CHATBOT_DB_NAME = os.getenv("CHATBOT_DB_NAME", "chatbotDB")
    
    # Collections trong chatbot database
    CONVERSATIONS_COLLECTION = "conversations"
    MESSAGES_COLLECTION = "messages"
    FEEDBACK_COLLECTION = "feedback"
    USERS_COLLECTION = "users"
    ANALYTICS_COLLECTION = "analytics"
    
    # Cấu hình khác
    MAX_MESSAGE_LENGTH = 1000
    SESSION_TIMEOUT = 3600  # 1 giờ
    MAX_CONVERSATIONS_PER_USER = 100
    
    # API Keys
    FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID")
    FACEBOOK_APP_SECRET = os.getenv("FACEBOOK_APP_SECRET")
    FACEBOOK_VERIFY_TOKEN = os.getenv("FACEBOOK_VERIFY_TOKEN")
    FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
    
    # Server config
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # Model config
    MODEL_PATH = os.getenv("MODEL_PATH", "./models")
    FALLBACK_MODEL = "distilbert-base-uncased"
    MAX_LENGTH = 512

    # Training config
    TRAINING_EPOCHS = int(os.getenv("TRAINING_EPOCHS", 10))
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 8))
    LEARNING_RATE = float(os.getenv("LEARNING_RATE", 5e-5))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "chatbot_api.log")
