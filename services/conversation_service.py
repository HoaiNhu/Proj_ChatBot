from logic.intent_rules import INTENT_RULES
from logic.context_rules import SHORT_QUESTION_RULES
from logic.intent_list import INTENT_LIST
from services.nlp_service import NLPService
import re
from config.config_chatbot import ChatbotConfig
from pymongo import MongoClient

store_client = MongoClient(ChatbotConfig.STORE_MONGO_URI)
store_db = store_client[ChatbotConfig.STORE_DB_NAME]

class ConversationService:
    def __init__(self, model_path):
        self.nlp_service = NLPService(model_path)
        self.conversation_context = {}  # Lưu context của cuộc hội thoại

    def detect_intent_logic(self, text):
        text_lower = text.lower()
        
        # Kiểm tra context rules trước (cho câu hỏi ngắn gọn)
        context_intent = self.check_context_rules(text_lower)
        if context_intent:
            return context_intent, 0.95  # Context intent, confidence cao
        
        # Kiểm tra các pattern đặc biệt trước
        if "giá dưới" in text_lower or "giá trên" in text_lower or "giá từ" in text_lower:
            return "suggest_cake", 1.0
        
        if "bảo quản" in text_lower or "giữ lạnh" in text_lower or "để được bao lâu" in text_lower:
            return "ask_preservation", 1.0
        
        # Kiểm tra intent rules thông thường
        for rule in INTENT_RULES:
            if any(keyword in text_lower for keyword in rule["keywords"]):
                return rule["intent"], 1.0  # Logic intent, confidence 1.0
        return None, None

    def check_context_rules(self, text_lower):
        """Cải thiện logic kiểm tra context rules"""
        # Nếu có tên bánh mới trong message, cập nhật context trước
        self.has_different_cake_name(text_lower)
        
        # Kiểm tra xem có phải câu hỏi ngắn gọn không
        if not self.is_short_question(text_lower):
            return None
            
        # Nếu là câu hỏi ngắn gọn và có context, trả về intent tương ứng
        for rule in SHORT_QUESTION_RULES:
            if rule.get('requires_context', False):
                pattern_matches = 0
                for pattern_word in rule["pattern"]:
                    if pattern_word in text_lower:
                        pattern_matches += 1
                
                # Nếu match được pattern và có context, trả về intent
                if pattern_matches > 0 and self.conversation_context.get('current_cake'):
                    return rule["context_intent"]
        
        return None

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
        if bot_response:
            self.conversation_context['last_bot_response'] = bot_response
        
        # Extract thông tin từ user_message
        self.extract_entities(user_message)
        
        # Lưu context theo thời gian (giữ 5 câu gần nhất)
        if 'message_history' not in self.conversation_context:
            self.conversation_context['message_history'] = []
        
        # Chỉ thêm vào history nếu có bot_response
        if bot_response:
            self.conversation_context['message_history'].append({
                'user': user_message,
                'intent': detected_intent,
                'bot': bot_response
            })
            
            # Giữ chỉ 5 câu gần nhất
            if len(self.conversation_context['message_history']) > 5:
                self.conversation_context['message_history'] = self.conversation_context['message_history'][-5:]

    def extract_entities(self, user_message):
        text_lower = user_message.lower()

        # LUÔN tìm và cập nhật tên bánh nếu có trong message
        found_cake = None
        for prod in store_db['products'].find():
            if prod.get('productName'):
                cake_name_lower = prod['productName'].lower()
                if cake_name_lower in text_lower:
                    found_cake = prod
                    break
        
        # Nếu tìm thấy bánh mới, LUÔN cập nhật context
        if found_cake:
            self.conversation_context['current_cake'] = found_cake['productName']
            self.conversation_context['current_cake_info'] = found_cake
            print(f"DEBUG - extract_entities: Updated context to: {found_cake['productName']}")
        
        # Các extract khác giữ nguyên
        number_match = re.search(r'(\d+)\s*người', text_lower)
        if number_match:
            self.conversation_context['people_count'] = int(number_match.group(1))
        occasions = ['sinh nhật', 'cưới', 'tiệc', 'giáng sinh', 'tết', 'valentine']
        for occasion in occasions:
            if occasion in text_lower:
                self.conversation_context['occasion'] = occasion
                break
        cake_types = ['bánh kem', 'bánh ngọt', 'bánh mặn', 'combo', 'bánh trái cây']
        for cake_type in cake_types:
            if cake_type in text_lower:
                self.conversation_context['cake_type'] = cake_type
                break

    def is_short_question(self, text_lower):
        """Cải thiện logic kiểm tra câu hỏi ngắn gọn"""
        short_patterns = [
            ['giá', 'bao nhiêu'],
            ['bao nhiêu', 'tiền'],
            ['bao nhiêu', 'đ'],
            ['chi phí', 'bao nhiêu'],
            ['thành phần', 'gì'],
            ['làm từ', 'gì'],
            ['nguyên liệu', 'gì'],
            ['vị', 'gì'],
            ['hương vị', 'gì'],
            ['mùi vị', 'gì'],
            ['còn', 'khác'],
            ['bánh', 'khác'],
            ['loại', 'khác'],
            ['combo', 'nào'],
            ['gói', 'nào'],
            ['set', 'nào'],
            ['khuyến mãi', 'gì'],
            ['ưu đãi', 'gì'],
            ['giảm giá', 'gì'],
            ['giao', 'không'],
            ['ship', 'không'],
            ['vận chuyển', 'không']
        ]
        
        # Kiểm tra xem có match pattern nào không
        for pattern in short_patterns:
            if any(word in text_lower for word in pattern):
                return True
        return False

    def get_context_action(self, current_intent, user_message=None):
        """Cải thiện logic lấy context action"""
        context_action = {}
        msg = user_message if user_message is not None else self.conversation_context.get('last_user_message', '')
        
        # Ưu tiên tên bánh trong message hiện tại
        cake_name_in_msg = self.get_cake_name_from_message(msg)
        if cake_name_in_msg:
            context_action['cake_name'] = cake_name_in_msg
        elif self.conversation_context.get('current_cake'):
            context_action['cake_name'] = self.conversation_context['current_cake']
        
        # Xử lý các intent cụ thể với context
        if current_intent == "ask_price" and context_action.get('cake_name'):
            context_action['context_flag'] = 'price_after_suggest'
        elif current_intent == "ask_ingredient" and context_action.get('cake_name'):
            context_action['context_flag'] = 'ingredient_after_suggest'
        elif current_intent == "ask_combo" and 'people_count' in self.conversation_context:
            context_action['context_flag'] = 'combo_with_people'
            context_action['people_count'] = self.conversation_context['people_count']
        elif current_intent == "ask_combo" and context_action.get('cake_name'):
            context_action['context_flag'] = 'combo_with_cake'
        
        # Xử lý câu hỏi về bánh khác
        if "còn" in msg.lower() and "khác" in msg.lower():
            context_action['context_flag'] = 'suggest_more_cakes'
        
        return context_action if context_action else None

    def get_cake_name_from_message(self, user_message):
        """Trích xuất tên bánh cụ thể từ user_message nếu có"""
        if not user_message:
            return None
        text_lower = user_message.lower()

        for prod in store_db['products'].find():
            if prod.get('productName'):
                cake_name_lower = prod['productName'].lower()
                if cake_name_lower in text_lower:
                    return prod['productName']
        return None

    def has_different_cake_name(self, user_message):
        """Cải thiện logic kiểm tra bánh khác"""
        if not user_message:
            return False
            
        text_lower = user_message.lower()
        current_cake = self.conversation_context.get('current_cake', '').lower()

        for prod in store_db['products'].find():
            if prod.get('productName'):
                cake_name_lower = prod['productName'].lower()
                if cake_name_lower in text_lower and cake_name_lower != current_cake:
                    # Cập nhật context ngay lập tức khi phát hiện bánh khác
                    self.conversation_context['current_cake'] = prod['productName']
                    self.conversation_context['current_cake_info'] = prod
                    print(f"DEBUG - has_different_cake_name: Updated context to: {prod['productName']}")
                    return True
        return False

    def clear_context(self):
        """Xóa context khi bắt đầu cuộc hội thoại mới"""
        self.conversation_context = {}

    def get_intent_list(self):
        """Trả về danh sách các intent có thể nhận diện"""
        return INTENT_LIST
