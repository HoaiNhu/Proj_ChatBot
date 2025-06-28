from logic.intent_rules import INTENT_RULES
from logic.intent_list import INTENT_LIST
from services.nlp_service import NLPService
import re

class ConversationService:
    def __init__(self, model_path):
        self.nlp_service = NLPService(model_path)
        self.conversation_context = {}  # Lưu context của cuộc hội thoại

    def detect_intent_logic(self, text):
        text_lower = text.lower()
        for rule in INTENT_RULES:
            if any(keyword in text_lower for keyword in rule["keywords"]):
                return rule["intent"], 1.0  # Logic intent, confidence 1.0
        return None, None

    def detect_intent(self, text):
        # Ưu tiên luật logic trước, nếu không có thì dùng mô hình
        intent, confidence = self.detect_intent_logic(text)
        if intent:
            return intent, confidence
        # Dùng mô hình nếu không match luật
        intent_idx, conf = self.nlp_service.predict_intent(text)
        # Map index về intent string dùng INTENT_LIST
        if 0 <= intent_idx < len(INTENT_LIST):
            intent = INTENT_LIST[intent_idx]
        else:
            # Fallback về suggest_cake nếu index không hợp lệ
            intent = "suggest_cake"
            conf = 0.5
        return intent, conf

    def update_context(self, user_message, detected_intent, bot_response):
        """Cập nhật context của cuộc hội thoại"""
        # Lưu thông tin về câu hỏi và trả lời gần nhất
        self.conversation_context['last_user_message'] = user_message
        self.conversation_context['last_intent'] = detected_intent
        self.conversation_context['last_bot_response'] = bot_response
        
        # Extract thông tin từ user_message
        self.extract_entities(user_message)
        
        # Lưu context theo thời gian (giữ 5 câu gần nhất)
        if 'message_history' not in self.conversation_context:
            self.conversation_context['message_history'] = []
        
        self.conversation_context['message_history'].append({
            'user': user_message,
            'intent': detected_intent,
            'bot': bot_response
        })
        
        # Giữ chỉ 5 câu gần nhất
        if len(self.conversation_context['message_history']) > 5:
            self.conversation_context['message_history'] = self.conversation_context['message_history'][-5:]

    def extract_entities(self, user_message):
        """Trích xuất thông tin từ user_message"""
        text_lower = user_message.lower()
        
        # Extract tên bánh
        from config.config_chatbot import ChatbotConfig
        from pymongo import MongoClient
        store_client = MongoClient(ChatbotConfig.STORE_MONGO_URI)
        store_db = store_client[ChatbotConfig.STORE_DB_NAME]
        
        for prod in store_db['products'].find():
            if prod.get('productName') and prod['productName'].lower() in text_lower:
                self.conversation_context['current_cake'] = prod['productName']
                self.conversation_context['current_cake_info'] = prod
                break
        
        # Extract số lượng người
        number_match = re.search(r'(\d+)\s*người', text_lower)
        if number_match:
            self.conversation_context['people_count'] = int(number_match.group(1))
        
        # Extract dịp lễ
        occasions = ['sinh nhật', 'cưới', 'tiệc', 'giáng sinh', 'tết', 'valentine']
        for occasion in occasions:
            if occasion in text_lower:
                self.conversation_context['occasion'] = occasion
                break
        
        # Extract loại bánh
        cake_types = ['bánh kem', 'bánh ngọt', 'bánh mặn', 'combo', 'bánh trái cây']
        for cake_type in cake_types:
            if cake_type in text_lower:
                self.conversation_context['cake_type'] = cake_type
                break

    def get_context_action(self, current_intent):
        """Xác định action dựa trên context"""
        context_action = {}
        
        # Nếu user hỏi về combo sau khi đã hỏi số người
        if current_intent == "ask_combo" and 'people_count' in self.conversation_context:
            context_action['context_flag'] = 'combo_with_people'
            context_action['people_count'] = self.conversation_context['people_count']
        
        # Nếu user hỏi thành phần sau khi đã được gợi ý bánh
        elif current_intent == "ask_ingredient" and 'current_cake' in self.conversation_context:
            context_action['context_flag'] = 'ingredient_after_suggest'
            context_action['cake_name'] = self.conversation_context['current_cake']
        
        # Nếu user hỏi giá sau khi đã được gợi ý bánh
        elif current_intent == "ask_price" and 'current_cake' in self.conversation_context:
            context_action['context_flag'] = 'price_after_suggest'
            context_action['cake_name'] = self.conversation_context['current_cake']
        
        # Nếu user hỏi "còn bánh khác không"
        elif "còn" in self.conversation_context.get('last_user_message', '').lower() and "khác" in self.conversation_context.get('last_user_message', '').lower():
            context_action['context_flag'] = 'suggest_more_cakes'
        
        # Nếu user hỏi về combo sau khi đã hỏi về bánh
        elif current_intent == "ask_combo" and 'current_cake' in self.conversation_context:
            context_action['context_flag'] = 'combo_with_cake'
            context_action['cake_name'] = self.conversation_context['current_cake']
        
        return context_action if context_action else None

    def clear_context(self):
        """Xóa context khi bắt đầu cuộc hội thoại mới"""
        self.conversation_context = {}

    def get_intent_list(self):
        """Trả về danh sách các intent có thể nhận diện"""
        return INTENT_LIST
