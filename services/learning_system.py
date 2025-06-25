import json
import os
from datetime import datetime, timedelta
from pymongo import MongoClient
from services.conversation_service import ConversationService
from config.config_chatbot import ChatbotConfig
from utils.logger import logger

class LearningSystem:
    def __init__(self, db):
        self.db = db
        self.chats_collection = db['conversation']  # Đổi từ 'chats' sang 'conversation'
        self.feedback_collection = db['feedback']
        self.learning_data_file = 'learning_data.json'
        self.intent_detector = ConversationService(model_path=ChatbotConfig.MODEL_PATH)
        
    def collect_conversation_data(self, user_input, bot_response, intent=None, confidence=None):
        """Thu thập dữ liệu từ cuộc trò chuyện"""
        try:
            conversation_data = {
                'user_input': user_input,
                'bot_response': bot_response,
                'intent': intent,
                'confidence': confidence,
                'timestamp': datetime.now(),
                'processed': False
            }
            
            self.chats_collection.insert_one(conversation_data)
            logger.info(f"Đã lưu cuộc trò chuyện: {user_input[:50]}...")
            
        except Exception as e:
            logger.error(f"Lỗi khi lưu cuộc trò chuyện: {e}")
    
    def collect_feedback(self, user_input, bot_response, is_helpful, feedback_text=None):
        """Thu thập phản hồi từ người dùng"""
        try:
            feedback_data = {
                'user_input': user_input,
                'bot_response': bot_response,
                'is_helpful': is_helpful,
                'feedback_text': feedback_text,
                'timestamp': datetime.now()
            }
            
            self.feedback_collection.insert_one(feedback_data)
            logger.info(f"Đã lưu phản hồi: {'Hữu ích' if is_helpful else 'Không hữu ích'}")
            
        except Exception as e:
            logger.error(f"Lỗi khi lưu phản hồi: {e}")
    
    def analyze_conversations(self, days_back=7):
        """Phân tích cuộc trò chuyện để cải thiện mô hình"""
        try:
            # Lấy cuộc trò chuyện trong 7 ngày qua
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            # Lấy cuộc trò chuyện chưa xử lý
            unprocessed_chats = self.chats_collection.find({
                'timestamp': {'$gte': cutoff_date},
                'processed': False
            })
            
            new_training_data = []
            
            for chat in unprocessed_chats:
                # Nhận diện intent từ user_input (không dùng bot_response nữa)
                intent, _ = self.intent_detector.detect_intent(chat['user_input'])
                if intent:
                    new_training_data.append({
                        'text': chat['user_input'],
                        'intent': intent
                    })
                
                # Đánh dấu đã xử lý
                self.chats_collection.update_one(
                    {'_id': chat['_id']},
                    {'$set': {'processed': True}}
                )
            
            # Lưu dữ liệu học tập mới
            if new_training_data:
                self._save_learning_data(new_training_data)
                logger.info(f"Đã tạo {len(new_training_data)} mẫu dữ liệu học tập mới")
            
            return new_training_data
            
        except Exception as e:
            logger.error(f"Lỗi khi phân tích cuộc trò chuyện: {e}")
            return []
    
    def _save_learning_data(self, new_data):
        """Lưu dữ liệu học tập mới"""
        try:
            # Đọc dữ liệu hiện tại
            existing_data = []
            if os.path.exists(self.learning_data_file):
                with open(self.learning_data_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            
            # Thêm dữ liệu mới
            existing_data.extend(new_data)
            
            # Lưu lại
            with open(self.learning_data_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"Lỗi khi lưu dữ liệu học tập: {e}")
    
    def get_performance_metrics(self, days_back=30):
        """Lấy số liệu hiệu suất của chatbot"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            # Tổng số cuộc trò chuyện
            total_conversations = self.chats_collection.count_documents({
                'timestamp': {'$gte': cutoff_date}
            })
            
            # Số phản hồi hữu ích
            helpful_feedback = self.feedback_collection.count_documents({
                'timestamp': {'$gte': cutoff_date},
                'is_helpful': True
            })
            
            # Số phản hồi không hữu ích
            unhelpful_feedback = self.feedback_collection.count_documents({
                'timestamp': {'$gte': cutoff_date},
                'is_helpful': False
            })
            
            # Tính tỷ lệ hài lòng
            total_feedback = helpful_feedback + unhelpful_feedback
            satisfaction_rate = (helpful_feedback / total_feedback * 100) if total_feedback > 0 else 0
            
            return {
                'total_conversations': total_conversations,
                'helpful_feedback': helpful_feedback,
                'unhelpful_feedback': unhelpful_feedback,
                'satisfaction_rate': round(satisfaction_rate, 2)
            }
            
        except Exception as e:
            logger.error(f"Lỗi khi lấy số liệu hiệu suất: {e}")
            return {}