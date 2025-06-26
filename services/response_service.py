import random
from logic.intent_rules import INTENT_RESPONSES  # chỉ import INTENT_RESPONSES
from logic.intent_list import INTENT_LIST        # import INTENT_LIST từ intent_list
from config.config_chatbot import ChatbotConfig
from pymongo import MongoClient

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

# Nếu bạn dùng class ResponseService, hãy cập nhật lại hàm get_response:
class ResponseService:
    def get_response(self, intent, user_message):
        return get_dynamic_response(intent, user_message)