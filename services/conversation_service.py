from logic.intent_rules import INTENT_RULES
from services.nlp_service import NLPService

class ConversationService:
    def __init__(self, model_path):
        self.nlp_service = NLPService(model_path)

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
        # Map index về intent string
        intent_map = {
            0: "suggest_cake",
            1: "ask_price",
            2: "connect_staff",
            3: "ask_promotion",
            4: "check_order",
            5: "custom_cake"
        }
        return intent_map.get(intent_idx, None), conf
