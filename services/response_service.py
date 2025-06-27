import random
from logic.intent_rules import INTENT_RESPONSES  # chỉ import INTENT_RESPONSES
from logic.intent_list import INTENT_LIST        # import INTENT_LIST từ intent_list
from config.config_chatbot import ChatbotConfig
from pymongo import MongoClient
from .response_templates import (
    SUGGEST_CAKE_TEMPLATES, ASK_PRICE_TEMPLATES, ASK_PROMO_TEMPLATES, ASK_INGREDIENT_TEMPLATES,
    ASK_ADDRESS_TEMPLATES, ASK_OPENING_TEMPLATES, ASK_CONTACT_TEMPLATES, ASK_FEEDBACK_TEMPLATES,
    ASK_COMBO_TEMPLATES, ASK_DELIVERY_TEMPLATES, ASK_NUTRITION_TEMPLATES, ASK_FOR_KIDS_TEMPLATES,
    CUSTOM_CAKE_TEMPLATES, CONNECT_STAFF_TEMPLATES, CHECK_ORDER_TEMPLATES, ASK_PAYMENT_TEMPLATES,
    ASK_PRESERVATION_TEMPLATES, ASK_RETURN_TEMPLATES, ASK_SPECIAL_EVENT_TEMPLATES, ASK_LOYALTY_TEMPLATES,
    ASK_INVOICE_TEMPLATES, ASK_PURCHASE_HISTORY_TEMPLATES
)

# Kết nối MongoDB cửa hàng để lấy dữ liệu động
store_client = MongoClient(ChatbotConfig.STORE_MONGO_URI)
store_db = store_client[ChatbotConfig.STORE_DB_NAME]

def get_dynamic_response(intent, user_message):
    # Nếu intent là index, chuyển sang intent name
    if isinstance(intent, int):
        if 0 <= intent < len(INTENT_LIST):
            intent_name = INTENT_LIST[intent]
        else:
            intent_name = None
    else:
        intent_name = intent

    # Trả lời động cho một số intent
    if intent_name == "suggest_cake":
       # Tìm bánh theo từ khóa user hỏi
        keyword = user_message.lower()
        matched_cakes = list(store_db['products'].find({
            "$or": [
                {"productName": {"$regex": keyword, "$options": "i"}},
                {"productDescription": {"$regex": keyword, "$options": "i"}}
            ]
        }))
        if matched_cakes:
            cake_names = ", ".join([cake["productName"] for cake in matched_cakes if "productName" in cake])
            return f"Shop có các loại bánh phù hợp với yêu cầu của bạn: {cake_names}. Bạn muốn chọn loại nào?"
        # Nếu không tìm thấy, fallback về 3 bánh nổi bật
        cakes = list(store_db['products'].find({}, {"productName": 1}).limit(3))
        if cakes:
            cake_names = ", ".join([cake["productName"] for cake in cakes if "productName" in cake])
            return f"Shop gợi ý bạn thử các loại bánh: {cake_names}. Bạn thích loại nào?"
    elif intent_name == "ask_price":
        # Tìm tên sản phẩm trong user_message
        for prod in store_db['products'].find():
            if prod.get('productName') and prod['productName'].lower() in user_message.lower():
                price = prod.get('productPrice', 'không rõ')
                return f"Bánh {prod['productName']} có giá {price}đ."
        return "Bạn muốn hỏi giá loại bánh nào ạ?"
    elif intent_name == "ask_promotion":
        # Lấy khuyến mãi mới nhất
        promo = store_db['discounts'].find_one(sort=[("createdAt", -1)])
        if promo and promo.get('discountName'):
            return f"Khuyến mãi hiện tại: {promo['discountName']} giảm {promo.get('discountValue', '')}%."
    elif intent_name == "check_order":
        # Tìm mã đơn hàng trong user_message
        import re
        match = re.search(r"(ORD-\d+)", user_message)
        if match:
            order_code = match.group(1)
            order = store_db['orders'].find_one({"orderCode": order_code})
            if order:
                status = "đã giao" if order.get("isDelivered") else "chưa giao"
                return f"Đơn hàng {order_code} hiện tại {status}."
            else:
                return f"Không tìm thấy đơn hàng mã {order_code}."
        return "Bạn vui lòng cung cấp mã đơn hàng (ví dụ: ORD-xxxxxxx) để mình kiểm tra nhé!"
    elif intent_name == "ask_feedback":
        # Lấy đánh giá mới nhất
        rating = store_db['ratings'].find_one(sort=[("createdAt", -1)])
        if rating and rating.get('comment'):
            return f"Khách hàng nhận xét: \"{rating['comment']}\""
    elif intent_name == "ask_combo":
        # Gợi ý combo từ sản phẩm
        combos = list(store_db['products'].find({"productName": {"$regex": "combo", "$options": "i"}}, {"productName": 1}).limit(2))
        if combos:
            combo_names = ", ".join([c["productName"] for c in combos if "productName" in c])
            return f"Shop có các combo: {combo_names}. Bạn muốn tham khảo combo nào?"
    elif intent_name == "ask_ingredient":
        # Lấy mô tả sản phẩm
        for prod in store_db['products'].find():
            if prod.get('productName') and prod['productName'].lower() in user_message.lower():
                desc = prod.get('productDescription', '')
                return f"Thành phần bánh {prod['productName']}: {desc}"
        return "Bạn muốn hỏi thành phần của loại bánh nào ạ?"
    elif intent_name == "ask_new_cake":
        # Lấy sản phẩm mới nhất
        cake = store_db['products'].find_one(sort=[("createdAt", -1)])
        if cake and cake.get('productName'):
            return f"Bánh mới nhất của shop là: {cake['productName']}."
    elif intent_name == "ask_best_seller":
        # Lấy sản phẩm bán chạy nhất
        cake = store_db['products'].find_one(sort=[("totalRatings", -1)])
        if cake and cake.get('productName'):
            return f"Bánh bán chạy nhất hiện nay là: {cake['productName']}."
    elif intent_name == "ask_for_kids":
        # Gợi ý bánh cho trẻ em
        cat = store_db['categories'].find_one({"categoryName": {"$regex": "trẻ em|bé", "$options": "i"}})
        if cat and cat.get('categoryName'):
            return f"Shop có bánh dành cho trẻ em thuộc danh mục: {cat['categoryName']}."
    elif intent_name == "ask_nutrition":
        # Lấy thông tin dinh dưỡng
        for prod in store_db['products'].find():
            if prod.get('productName') and prod['productName'].lower() in user_message.lower():
                nutrition = prod.get('nutrition') or prod.get('productDescription')
                if nutrition:
                    return f"Thông tin dinh dưỡng bánh {prod['productName']}: {nutrition}"
        return "Bạn muốn hỏi dinh dưỡng của loại bánh nào ạ?"
    elif intent_name == "ask_address":
        # Gợi ý địa chỉ nếu có trường address trong db
        shop_info = store_db['shop_info'].find_one() if 'shop_info' in store_db.list_collection_names() else None
        if shop_info and shop_info.get('address'):
            return f"Địa chỉ shop: {shop_info['address']}"
    elif intent_name == "ask_opening_hours":
        # Gợi ý giờ mở cửa nếu có trường openingHours trong db
        shop_info = store_db['shop_info'].find_one() if 'shop_info' in store_db.list_collection_names() else None
        if shop_info and shop_info.get('openingHours'):
            return f"Giờ mở cửa: {shop_info['openingHours']}"
    # ... có thể mở rộng cho các intent khác ...

    # Fallback về INTENT_RESPONSES như cũ
    responses = INTENT_RESPONSES.get(intent_name)
    if responses:
        return random.choice(responses)
    # Nếu không có response mẫu, sinh câu trả lời động
    fallback_templates = [
        f"Shop hiện chưa có thông tin chi tiết về vấn đề này (intent: {intent_name}), bạn vui lòng để lại câu hỏi, shop sẽ hỗ trợ sau!",
        f"Shop sẽ kiểm tra lại thông tin về \"{user_message}\" và phản hồi bạn sớm nhất!",
        "Câu hỏi của bạn rất hay, shop sẽ bổ sung thông tin này sớm!",
        "Hiện tại shop chưa có câu trả lời chính xác, bạn vui lòng liên hệ hotline để được hỗ trợ nhanh nhất!",
        "Shop xin lỗi vì chưa hỗ trợ được câu hỏi này, bạn có thể hỏi lại theo cách khác hoặc để lại thông tin liên hệ nhé!"
    ]
    return random.choice(fallback_templates)

def generate_template_response(intent, entities, templates):
    if not templates:
        return None
    template = random.choice(templates)
    try:
        return template.format(**entities)
    except Exception:
        return None

class ResponseService:
    def get_response(self, intent, user_message, context_action=None, last_bot_intent=None):
        # Nếu có context_action (dict), sinh câu trả lời động dựa trên context
        if context_action:
            context_flag = context_action.get("context_flag")
            # Ví dụ: nếu context_flag là promotion_price thì trả lời giá + khuyến mãi
            if context_flag == "promotion_price":
                # Lấy giá và khuyến mãi động
                price_resp = self.get_price_response(user_message)
                promo_resp = self.get_promo_response()
                return f"Hiện tại shop đang có khuyến mãi! {price_resp} {promo_resp}"
            elif context_flag == "ingredient_after_suggest":
                return self.get_ingredient_response(user_message)
            elif context_flag == "price_after_suggest":
                return self.get_price_response(user_message)
            elif context_flag == "promotion_ingredient":
                promo_resp = self.get_promo_response()
                ingredient_resp = self.get_ingredient_response(user_message)
                return f"Bánh này đang có ưu đãi! {ingredient_resp} {promo_resp}"
            # ... mở rộng các context_flag khác ...
            # Nếu không match context_flag nào, fallback về intent hiện tại
            return self.get_intent_template_response(intent, user_message)
        # Nếu không có context_action, xử lý như cũ
        return self.get_intent_template_response(intent, user_message)

    def get_intent_template_response(self, intent, user_message):
        # intent có thể là index hoặc tên
        intent_name = intent
        if isinstance(intent, int):
            from logic.intent_list import INTENT_LIST
            if 0 <= intent < len(INTENT_LIST):
                intent_name = INTENT_LIST[intent]
        # Lấy data động từ MongoDB
        from config.config_chatbot import ChatbotConfig
        from pymongo import MongoClient
        store_client = MongoClient(ChatbotConfig.STORE_MONGO_URI)
        store_db = store_client[ChatbotConfig.STORE_DB_NAME]
        # Tùy intent mà lấy data và template phù hợp
        if intent_name == "suggest_cake":
            cake = store_db['products'].find_one(sort=[("totalRatings", -1)])
            entities = {
                "cake_name": cake["productName"] if cake else "bánh ngon",
                "flavor": "socola",  # TODO: extract từ user_message nếu có
                "occasion": "sinh nhật"  # TODO: extract từ context nếu có
            }
            resp = generate_template_response("suggest_cake", entities, SUGGEST_CAKE_TEMPLATES)
            if resp:
                return resp
        elif intent_name == "ask_price":
            return self.get_price_response(user_message)
        elif intent_name == "ask_promotion":
            return self.get_promo_response()
        elif intent_name == "ask_ingredient":
            return self.get_ingredient_response(user_message)
        elif intent_name == "ask_address":
            shop_info = store_db['shop_info'].find_one() if 'shop_info' in store_db.list_collection_names() else None
            entities = {"address": shop_info.get("address", "123 Đường Bánh Ngon") if shop_info else "123 Đường Bánh Ngon"}
            resp = generate_template_response("ask_address", entities, ASK_ADDRESS_TEMPLATES)
            if resp:
                return resp
        elif intent_name == "ask_opening_hours":
            shop_info = store_db['shop_info'].find_one() if 'shop_info' in store_db.list_collection_names() else None
            entities = {"open_hour": shop_info.get("openingHours", "7h-21h") if shop_info else "7h-21h"}
            resp = generate_template_response("ask_opening_hours", entities, ASK_OPENING_TEMPLATES)
            if resp:
                return resp
        elif intent_name == "ask_contact":
            shop_info = store_db['shop_info'].find_one() if 'shop_info' in store_db.list_collection_names() else None
            entities = {
                "phone": shop_info.get("phone", "0123 456 789") if shop_info else "0123 456 789",
                "email": shop_info.get("email", "info@avocadocake.vn") if shop_info else "info@avocadocake.vn"
            }
            resp = generate_template_response("ask_contact", entities, ASK_CONTACT_TEMPLATES)
            if resp:
                return resp
        elif intent_name == "ask_feedback":
            resp = generate_template_response("ask_feedback", {}, ASK_FEEDBACK_TEMPLATES)
            if resp:
                return resp
        # ... có thể mở rộng cho các intent khác ...
        # Fallback về get_dynamic_response như cũ
        return get_dynamic_response(intent, user_message)

    def get_price_response(self, user_message):
        from config.config_chatbot import ChatbotConfig
        from pymongo import MongoClient
        store_client = MongoClient(ChatbotConfig.STORE_MONGO_URI)
        store_db = store_client[ChatbotConfig.STORE_DB_NAME]
        # Tìm tên sản phẩm trong user_message
        for prod in store_db['products'].find():
            if prod.get('productName') and prod['productName'].lower() in user_message.lower():
                entities = {"cake_name": prod['productName'], "price": prod.get('productPrice', 'không rõ')}
                resp = generate_template_response("ask_price", entities, ASK_PRICE_TEMPLATES)
                if resp:
                    return resp
        # Nếu không tìm thấy, fallback về mẫu chung
        cake = store_db['products'].find_one(sort=[("totalRatings", -1)])
        entities = {"cake_name": cake["productName"] if cake else "bánh ngon", "price": cake.get("productPrice", "200.000") if cake else "200.000"}
        resp = generate_template_response("ask_price", entities, ASK_PRICE_TEMPLATES)
        if resp:
            return resp
        return "Bạn muốn hỏi giá loại bánh nào ạ?"

    def get_promo_response(self):
        from config.config_chatbot import ChatbotConfig
        from pymongo import MongoClient
        store_client = MongoClient(ChatbotConfig.STORE_MONGO_URI)
        store_db = store_client[ChatbotConfig.STORE_DB_NAME]
        promo = store_db['discounts'].find_one(sort=[("createdAt", -1)])
        entities = {
            "promo_name": promo.get("discountName", "ưu đãi đặc biệt") if promo else "ưu đãi đặc biệt",
            "promo_value": promo.get("discountValue", "10") if promo else "10"
        }
        resp = generate_template_response("ask_promotion", entities, ASK_PROMO_TEMPLATES)
        if resp:
            return resp
        return "Hiện tại shop có nhiều chương trình khuyến mãi hấp dẫn, bạn muốn biết về ưu đãi nào?"

    def get_ingredient_response(self, user_message):
        from config.config_chatbot import ChatbotConfig
        from pymongo import MongoClient
        store_client = MongoClient(ChatbotConfig.STORE_MONGO_URI)
        store_db = store_client[ChatbotConfig.STORE_DB_NAME]
        for prod in store_db['products'].find():
            if prod.get('productName') and prod['productName'].lower() in user_message.lower():
                entities = {"cake_name": prod['productName'], "ingredient": prod.get('productDescription', '')}
                resp = generate_template_response("ask_ingredient", entities, ASK_INGREDIENT_TEMPLATES)
                if resp:
                    return resp
        # Nếu không tìm thấy, fallback về mẫu chung
        cake = store_db['products'].find_one(sort=[("totalRatings", -1)])
        entities = {"cake_name": cake["productName"] if cake else "bánh ngon", "ingredient": cake.get("productDescription", "bơ, sữa, trứng") if cake else "bơ, sữa, trứng"}
        resp = generate_template_response("ask_ingredient", entities, ASK_INGREDIENT_TEMPLATES)
        if resp:
            return resp
        return "Bạn muốn hỏi thành phần của loại bánh nào ạ?"