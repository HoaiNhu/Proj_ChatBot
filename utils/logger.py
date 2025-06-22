import logging
import os
from datetime import datetime
from config.config_chatbot import Config

def setup_logger():
    """Thiết lập logger cho ứng dụng"""
    
    # Tạo thư mục logs nếu chưa có
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Cấu hình logger
    logger = logging.getLogger('chatbot')
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    # Tạo formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler cho file
    file_handler = logging.FileHandler(
        os.path.join(log_dir, f'chatbot_{datetime.now().strftime("%Y%m%d")}.log'),
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # Handler cho console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    
    # Thêm handlers vào logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Tạo logger instance
logger = setup_logger() 