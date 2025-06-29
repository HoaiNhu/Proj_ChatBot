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

def normalize_text(text):
    """Chuẩn hóa text để so sánh, loại bỏ dấu và khoảng trắng thừa"""
    if not text:
        return ""
    import unicodedata
    # Loại bỏ dấu tiếng Việt
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    # Chuyển về lowercase và loại bỏ khoảng trắng thừa
    return text.lower().strip()

def fix_duplicate_cake_name(response):
    """Sửa lỗi lặp từ 'Bánh' trong response"""
    if not response:
        return response
    # Sửa "Bánh Bánh" thành "Bánh"
    response = response.replace("Bánh Bánh", "Bánh")
    # Sửa "bánh Bánh" thành "bánh"
    response = response.replace("bánh Bánh", "bánh")
    return response

def get_dynamic_response(intent, user_message, context_action=None):
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
        # Kiểm tra xem có phải hỏi bánh theo giá không
        text_lower = user_message.lower()
        
        # Tìm bánh theo khoảng giá
        price_match = None
        if "dưới" in text_lower and any(char.isdigit() for char in text_lower):
            # Tìm số trong câu
            import re
            numbers = re.findall(r'\d+', text_lower)
            if numbers:
                max_price = int(numbers[0]) * 1000  # Chuyển k thành nghìn
                if "k" in text_lower or "nghìn" in text_lower:
                    max_price = int(numbers[0]) * 1000
                elif "tr" in text_lower or "triệu" in text_lower:
                    max_price = int(numbers[0]) * 1000000
                else:
                    max_price = int(numbers[0])
                
                # Tìm bánh trong khoảng giá
                affordable_cakes = list(store_db['products'].find({
                    "productPrice": {"$lte": max_price}
                }, {"productName": 1, "productPrice": 1, "averageRating": 1}).sort([("averageRating", -1)]).limit(5))
                
                if affordable_cakes:
                    cake_info = []
                    for cake in affordable_cakes:
                        name = cake.get("productName", "")
                        price = cake.get("productPrice", 0)
                        rating = cake.get("averageRating", 0)
                        if name:
                            cake_info.append(f"{name} ({price:,}đ, ⭐{rating})")
                    
                    cake_list = ", ".join(cake_info)
                    return f"Shop có các loại bánh dưới {max_price:,}đ: {cake_list}. Bạn thích loại nào?"
                else:
                    return f"Hiện tại shop chưa có bánh nào dưới {max_price:,}đ. Bạn có thể tham khảo các loại bánh khác nhé!"
        
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
        
        # Nếu không tìm thấy, lấy 3-5 bánh ngẫu nhiên từ top 10 bánh có rating cao
        top_cakes = list(store_db['products'].find({}, {"productName": 1, "productPrice": 1, "averageRating": 1}).sort([("averageRating", -1)]).limit(10))
        if top_cakes:
            # Chọn ngẫu nhiên 3-5 bánh từ top 10
            selected_cakes = random.sample(top_cakes, min(3, len(top_cakes)))
            cake_info = []
            for cake in selected_cakes:
                name = cake.get("productName", "")
                price = cake.get("productPrice", "")
                rating = cake.get("averageRating", 0)
                if name:
                    cake_info.append(f"{name} ({price:,}đ, ⭐{rating})")
            
            cake_list = ", ".join(cake_info)
            return f"Shop gợi ý bạn thử các loại bánh: {cake_list}. Bạn thích loại nào?"
        
        # Fallback nếu không có bánh nào
        return "Hiện tại shop đang cập nhật menu, bạn vui lòng liên hệ hotline để được tư vấn nhé!"
        
    elif intent_name == "ask_preservation":
        # Trả lời về cách bảo quản bánh
        return "Cách bảo quản bánh: Bánh kem nên để trong tủ lạnh từ 2-4°C, có thể bảo quản được 3-5 ngày. Bánh ngọt để ở nhiệt độ phòng được 2-3 ngày. Khi vận chuyển xa, shop sẽ đóng gói đặc biệt với đá khô để giữ lạnh."
        
    elif intent_name == "ask_price":
        # LUÔN kiểm tra tên bánh trong user_message trước (chuẩn hóa)
        msg_norm = normalize_text(user_message)
        for prod in store_db['products'].find():
            if prod.get('productName'):
                cake_name_norm = normalize_text(prod['productName'])
                if cake_name_norm in msg_norm:
                    price = prod.get('productPrice', 'không rõ')
                    return fix_duplicate_cake_name(f"Bánh {prod['productName']} có giá {price:,}đ.")
        
        # Nếu không tìm thấy trong message, mới dùng context_action
        if context_action and context_action.get("cake_name"):
            cake_name = context_action.get("cake_name", "")
            if cake_name:
                cake = store_db['products'].find_one({"productName": cake_name})
                if cake:
                    price = cake.get('productPrice', 'không rõ')
                    return fix_duplicate_cake_name(f"Bánh {cake_name} có giá {price:,}đ.")
        
        return "Bạn muốn hỏi giá loại bánh nào ạ?"
        
    elif intent_name == "ask_promotion":
        # Lấy khuyến mãi mới nhất
        promo = store_db['discounts'].find_one(sort=[("createdAt", -1)])
        if promo and promo.get('discountName'):
            return f"Khuyến mãi hiện tại: {promo['discountName']} giảm {promo.get('discountValue', '')}%."
        return "Hiện tại shop có nhiều chương trình khuyến mãi hấp dẫn, bạn muốn biết về ưu đãi nào?"
        
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
        return "Shop luôn cố gắng cải thiện chất lượng phục vụ, bạn có thể để lại đánh giá nhé!"
        
    elif intent_name == "ask_combo":
        # Gợi ý combo từ sản phẩm
        combos = list(store_db['products'].find({"productName": {"$regex": "combo", "$options": "i"}}, {"productName": 1, "productPrice": 1}).limit(3))
        if combos:
            combo_info = []
            for combo in combos:
                name = combo.get("productName", "")
                price = combo.get("productPrice", "")
                if name:
                    combo_info.append(f"{name} ({price:,}đ)")
            combo_list = ", ".join(combo_info)
            return f"Shop có các combo: {combo_list}. Bạn muốn tham khảo combo nào?"
        
        # Nếu không có combo, tạo combo từ các bánh phổ biến
        popular_cakes = list(store_db['products'].find({}, {"productName": 1, "productPrice": 1}).sort([("averageRating", -1)]).limit(2))
        if len(popular_cakes) >= 2:
            cake1 = popular_cakes[0].get("productName", "")
            cake2 = popular_cakes[1].get("productName", "")
            return f"Shop có thể tạo combo từ {cake1} và {cake2} với giá ưu đãi. Bạn quan tâm không?"
        
        return "Shop có thể tạo combo theo yêu cầu của bạn, bạn muốn combo gì ạ?"
        
    elif intent_name == "ask_ingredient":
        # Lấy mô tả sản phẩm
        for prod in store_db['products'].find():
            if prod.get('productName') and prod['productName'].lower() in user_message.lower():
                desc = prod.get('productDescription', '')
                return fix_duplicate_cake_name(f"Thành phần bánh {prod['productName']}: {desc}")
        return "Bạn muốn hỏi thành phần của loại bánh nào ạ?"
        
    elif intent_name == "ask_new_cake":
        # Lấy sản phẩm mới nhất
        cake = store_db['products'].find_one(sort=[("createdAt", -1)])
        if cake and cake.get('productName'):
            return fix_duplicate_cake_name(f"Bánh mới nhất của shop là: {cake['productName']}.")
        return "Shop thường xuyên cập nhật menu mới, bạn có thể ghé shop để thưởng thức!"
        
    elif intent_name == "ask_best_seller":
        # Lấy sản phẩm bán chạy nhất
        cake = store_db['products'].find_one(sort=[("totalRatings", -1)])
        if cake and cake.get('productName'):
            return fix_duplicate_cake_name(f"Bánh bán chạy nhất hiện nay là: {cake['productName']}.")
        return "Shop có nhiều loại bánh được khách hàng yêu thích, bạn muốn thử loại nào?"
        
    elif intent_name == "ask_for_kids":
        # Gợi ý bánh cho trẻ em
        cat = store_db['categories'].find_one({"categoryName": {"$regex": "trẻ em|bé", "$options": "i"}})
        if cat and cat.get('categoryName'):
            return f"Shop có bánh dành cho trẻ em thuộc danh mục: {cat['categoryName']}."
        return "Shop có nhiều loại bánh phù hợp với trẻ em, bạn muốn tham khảo loại nào?"
        
    elif intent_name == "ask_nutrition":
        # Lấy thông tin dinh dưỡng
        for prod in store_db['products'].find():
            if prod.get('productName') and prod['productName'].lower() in user_message.lower():
                nutrition = prod.get('nutrition') or prod.get('productDescription')
                if nutrition:
                    return fix_duplicate_cake_name(f"Thông tin dinh dưỡng bánh {prod['productName']}: {nutrition}")
        return "Bạn muốn hỏi dinh dưỡng của loại bánh nào ạ?"
        
    elif intent_name == "ask_address":
        # Gợi ý địa chỉ nếu có trường address trong db
        shop_info = store_db['shop_info'].find_one() if 'shop_info' in store_db.list_collection_names() else None
        if shop_info and shop_info.get('address'):
            return f"Địa chỉ shop: {shop_info['address']}"
        return "Shop có địa chỉ tại 123 Đường Bánh Ngon, bạn có thể ghé thăm!"
        
    elif intent_name == "ask_opening_hours":
        # Gợi ý giờ mở cửa nếu có trường openingHours trong db
        shop_info = store_db['shop_info'].find_one() if 'shop_info' in store_db.list_collection_names() else None
        if shop_info and shop_info.get('openingHours'):
            return f"Giờ mở cửa: {shop_info['openingHours']}"
        return "Shop mở cửa từ 7h sáng đến 21h tối, bạn có thể ghé thăm bất cứ lúc nào!"
        
    # ... có thể mở rộng cho các intent khác ...

    # Fallback về INTENT_RESPONSES như cũ
    responses = INTENT_RESPONSES.get(intent_name)
    if responses:
        return random.choice(responses)
    # Nếu không có response mẫu, sinh câu trả lời động
    fallback_templates = [
        f"Shop hiện chưa có thông tin chi tiết về vấn đề này, bạn vui lòng để lại câu hỏi, shop sẽ hỗ trợ sau!",
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

    def get_cake_name_from_message(self, user_message):
        if not user_message:
            return None
        text_lower = user_message.lower()

        for prod in store_db['products'].find():
            if prod.get('productName'):
                cake_name_lower = prod['productName'].lower()
                if cake_name_lower in text_lower:
                    return prod['productName']
        return None

    def get_response(self, intent, user_message, context_action=None, last_bot_intent=None):
        """Cải thiện logic xử lý response với context tốt hơn"""
        # Nếu intent là index, chuyển sang intent name
        if isinstance(intent, int):
            if 0 <= intent < len(INTENT_LIST):
                intent_name = INTENT_LIST[intent]
            else:
                intent_name = "suggest_cake"
        else:
            intent_name = intent

        # Xử lý các câu hỏi ngắn gọn với context
        if self.is_short_question_with_context(intent_name, user_message, context_action):
            return self.handle_short_question_with_context(intent_name, user_message, context_action)
        
        # Xử lý response động cho các intent
        dynamic_response = get_dynamic_response(intent_name, user_message, context_action)
        if dynamic_response:
            return fix_duplicate_cake_name(dynamic_response)
        
        # Fallback về template response
        return self.get_intent_template_response(intent, user_message, context_action)

    def is_short_question_with_context(self, intent_name, user_message, context_action):
        """Kiểm tra xem có phải câu hỏi ngắn gọn cần context không"""
        short_questions = ["ask_price", "ask_ingredient", "ask_combo", "ask_promotion"]
        return intent_name in short_questions and context_action and context_action.get('cake_name')

    def handle_short_question_with_context(self, intent_name, user_message, context_action):
        """Xử lý câu hỏi ngắn gọn với context"""
        cake_name = context_action.get('cake_name')
        if not cake_name:
            return self.get_fallback_response(intent_name)
        
        # Tìm thông tin bánh từ database
        cake = store_db['products'].find_one({"productName": cake_name})
        if not cake:
            return self.get_fallback_response(intent_name)
        
        if intent_name == "ask_price":
            price = cake.get('productPrice', 'không rõ')
            return f"{cake_name} có giá {price:,}đ."
        
        elif intent_name == "ask_ingredient":
            desc = cake.get('productDescription', '')
            if desc:
                return f"Thành phần {cake_name}: {desc}"
            else:
                return f"Thành phần {cake_name}: Bột mì, đường, trứng, sữa tươi và các nguyên liệu tự nhiên khác."
        
        elif intent_name == "ask_combo":
            # Gợi ý combo với bánh hiện tại
            return f"Shop có thể tạo combo với {cake_name} và các loại bánh khác. Bạn muốn combo gì ạ?"
        
        elif intent_name == "ask_promotion":
            # Kiểm tra khuyến mãi cho bánh cụ thể
            promo = store_db['discounts'].find_one(sort=[("createdAt", -1)])
            if promo and promo.get('discountName'):
                return f"Hiện tại {cake_name} đang có khuyến mãi: {promo['discountName']} giảm {promo.get('discountValue', '')}%."
            else:
                return f"{cake_name} hiện tại chưa có khuyến mãi, nhưng shop có nhiều ưu đãi khác. Bạn quan tâm không?"
        
        return self.get_fallback_response(intent_name)

    def get_fallback_response(self, intent_name):
        """Trả về response fallback cho từng intent"""
        fallback_responses = {
            "ask_price": "Bạn muốn hỏi giá loại bánh nào ạ?",
            "ask_ingredient": "Bạn muốn hỏi thành phần của loại bánh nào ạ?",
            "ask_combo": "Shop có nhiều combo hấp dẫn, bạn muốn tham khảo combo nào?",
            "ask_promotion": "Shop có nhiều chương trình khuyến mãi, bạn muốn biết về ưu đãi nào?",
            "ask_delivery": "Shop có dịch vụ giao hàng, bạn muốn biết thông tin gì?",
            "ask_feedback": "Shop luôn cố gắng cải thiện chất lượng, bạn có thể để lại đánh giá nhé!"
        }
        return fallback_responses.get(intent_name, "Bạn cần tư vấn gì thêm không?")

    def get_intent_template_response(self, intent, user_message, context_action=None):
        # intent có thể là index hoặc tên
        intent_name = intent
        if isinstance(intent, int):
            from logic.intent_list import INTENT_LIST
            if 0 <= intent < len(INTENT_LIST):
                intent_name = INTENT_LIST[intent]
        
        # Sử dụng get_dynamic_response để tránh lặp lại logic
        dynamic_response = get_dynamic_response(intent, user_message, context_action)
        if dynamic_response:
            return dynamic_response
  

        
        # Tùy intent mà lấy data và template phù hợp
        if intent_name == "ask_address":
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

        # Tìm tên sản phẩm trong user_message
        for prod in store_db['products'].find():
            if prod.get('productName') and prod['productName'].lower() in user_message.lower():
                entities = {"cake_name": prod['productName'], "price": f"{prod.get('productPrice', 'không rõ'):,}"}
                resp = generate_template_response("ask_price", entities, ASK_PRICE_TEMPLATES)
                if resp:
                    return fix_duplicate_cake_name(resp)
        # Nếu không tìm thấy, lấy bánh ngẫu nhiên từ top 5
        top_cakes = list(store_db['products'].find({}, {"productName": 1, "productPrice": 1}).sort([("averageRating", -1)]).limit(5))
        if top_cakes:
            cake = random.choice(top_cakes)
            entities = {"cake_name": cake.get("productName", "bánh ngon"), "price": f"{cake.get('productPrice', 200000):,}"}
            resp = generate_template_response("ask_price", entities, ASK_PRICE_TEMPLATES)
            if resp:
                return fix_duplicate_cake_name(resp)
        return "Bạn muốn hỏi giá loại bánh nào ạ?"

    def get_promo_response(self):
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
        for prod in store_db['products'].find():
            if prod.get('productName') and prod['productName'].lower() in user_message.lower():
                entities = {"cake_name": prod['productName'], "ingredient": prod.get('productDescription', '')}
                resp = generate_template_response("ask_ingredient", entities, ASK_INGREDIENT_TEMPLATES)
                if resp:
                    return fix_duplicate_cake_name(resp)
        # Nếu không tìm thấy, lấy bánh ngẫu nhiên từ top 5
        top_cakes = list(store_db['products'].find({}, {"productName": 1, "productDescription": 1}).sort([("averageRating", -1)]).limit(5))
        if top_cakes:
            cake = random.choice(top_cakes)
            entities = {"cake_name": cake.get("productName", "bánh ngon"), "ingredient": cake.get("productDescription", "bơ, sữa, trứng")}
            resp = generate_template_response("ask_ingredient", entities, ASK_INGREDIENT_TEMPLATES)
            if resp:
                return fix_duplicate_cake_name(resp)
        return "Bạn muốn hỏi thành phần của loại bánh nào ạ?"