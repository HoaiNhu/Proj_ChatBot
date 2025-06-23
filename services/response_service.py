import random
from logic.intent_rules import INTENT_RESPONSES

class ResponseService:
    def get_response(self, intent, user_input):
        # Nếu có intent, lấy response từ rule
        if intent in INTENT_RESPONSES:
            return random.choice(INTENT_RESPONSES[intent])
        # Nếu không có, trả về fallback
        return "Xin lỗi, tôi chưa hiểu ý bạn. Bạn có thể nói rõ hơn không?"