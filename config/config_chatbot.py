import os
from dotenv import load_dotenv

load_dotenv()

class ChatbotConfig:
    """Cấu hình riêng cho chatbot MongoDB"""
    
    # MongoDB cho chatbot (riêng biệt với MongoDB training)
    CHATBOT_MONGO_URI = os.getenv("CHATBOT_MONGO_URI", "mongodb://localhost:27017/chatbot_support")
    CHATBOT_DB_NAME = os.getenv("CHATBOT_DB_NAME", "chatbot_support")
    
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
    
    # Server config
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # Model config
    MODEL_PATH = os.getenv("MODEL_PATH", "./models")
    FALLBACK_MODEL = "distilbert-base-uncased"
    MAX_LENGTH = 512
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "chatbot_api.log") 