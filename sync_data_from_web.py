"""
Script để đồng bộ data từ MongoDB web bán bánh sang data.json cho training
Chạy script này trước khi train để có data mới nhất
"""
import json
from pymongo import MongoClient
from config.config_chatbot import ChatbotConfig
from datetime import datetime

def sync_data_from_web():
    """Lấy data mới từ MongoDB web và tạo training data"""
    print("🔄 Đang kết nối MongoDB web bán bánh...")
    
    # Kết nối MongoDB cửa hàng
    store_client = MongoClient(ChatbotConfig.STORE_MONGO_URI)
    store_db = store_client[ChatbotConfig.STORE_DB_NAME]
    
    training_data = []
    
    # 1. Tạo data từ tên bánh (intent: suggest_cake)
    print("📦 Lấy thông tin sản phẩm...")
    products = list(store_db['products'].find())
    for product in products:
        name = product.get('productName', '')
        if name:
            # Tạo nhiều biến thể câu hỏi cho mỗi bánh
            training_data.extend([
                {"text": f"Tôi muốn bánh {name}", "intent": "suggest_cake"},
                {"text": f"Gợi ý bánh {name} đi", "intent": "suggest_cake"},
                {"text": f"Shop có bánh {name} không?", "intent": "suggest_cake"},
                {"text": f"Bánh {name} có ngon không?", "intent": "suggest_cake"},
                {"text": f"Cho xin thông tin bánh {name}", "intent": "suggest_cake"},
                {"text": f"{name} giá bao nhiêu?", "intent": "ask_price"},
                {"text": f"Bánh {name} bao nhiêu tiền?", "intent": "ask_price"},
                {"text": f"Cho hỏi giá {name}", "intent": "ask_price"},
                {"text": f"{name} làm từ gì?", "intent": "ask_ingredient"},
                {"text": f"Thành phần {name} là gì?", "intent": "ask_ingredient"},
    ])
    
    # 2. Tạo data từ categories
    print("📂 Lấy thông tin danh mục...")
    categories = list(store_db['categories'].find())
    for category in categories:
        cat_name = category.get('categoryName', '')
        if cat_name:
            training_data.extend([
                {"text": f"Gợi ý bánh {cat_name}", "intent": "suggest_cake"},
                {"text": f"Shop có loại {cat_name} nào ngon?", "intent": "suggest_cake"},
                {"text": f"Tôi muốn xem bánh {cat_name}", "intent": "suggest_cake"},
            ])
    
    # 3. Tạo data từ khuyến mãi
    print("🎁 Lấy thông tin khuyến mãi...")
    discounts = list(store_db['discounts'].find())
    for discount in discounts:
        disc_name = discount.get('discountName', '')
        if disc_name:
            training_data.extend([
                {"text": f"Khuyến mãi {disc_name} thế nào?", "intent": "ask_promotion"},
                {"text": f"Cho hỏi về {disc_name}", "intent": "ask_promotion"},
                {"text": f"Có giảm giá {disc_name} không?", "intent": "ask_promotion"},
            ])
    
    # 4. Thêm các intent cơ bản (giữ nguyên từ data cũ)
    print("📝 Thêm các intent cơ bản...")
    basic_intents = [
        # Greeting
        {"text": "Chào shop", "intent": "greeting"},
        {"text": "Hello", "intent": "greeting"},
        {"text": "Hi shop", "intent": "greeting"},
        {"text": "Chào bạn", "intent": "greeting"},
        {"text": "Xin chào", "intent": "greeting"},
        
        # Goodbye
        {"text": "Tạm biệt", "intent": "goodbye"},
        {"text": "Bye", "intent": "goodbye"},
        {"text": "Hẹn gặp lại", "intent": "goodbye"},
        
        # Ask address
        {"text": "Shop ở đâu?", "intent": "ask_address"},
        {"text": "Địa chỉ shop", "intent": "ask_address"},
        {"text": "Cho địa chỉ", "intent": "ask_address"},
        
        # Ask opening hours
        {"text": "Giờ mở cửa", "intent": "ask_opening_hours"},
        {"text": "Shop mở cửa lúc nào?", "intent": "ask_opening_hours"},
        
        # Ask contact
        {"text": "Số điện thoại shop", "intent": "ask_contact"},
        {"text": "Liên hệ shop", "intent": "ask_contact"},
        
        # Ask delivery
        {"text": "Shop có giao hàng không?", "intent": "ask_delivery"},
        {"text": "Giao hàng tận nơi không?", "intent": "ask_delivery"},
        
        # Check order
        {"text": "Kiểm tra đơn hàng", "intent": "check_order"},
        {"text": "Tra cứu đơn hàng", "intent": "check_order"},
        
        # Ask payment
        {"text": "Thanh toán thế nào?", "intent": "ask_payment"},
        {"text": "Phương thức thanh toán", "intent": "ask_payment"},
        
        # Connect staff
        {"text": "Kết nối nhân viên", "intent": "connect_staff"},
        {"text": "Nói chuyện với nhân viên", "intent": "connect_staff"},
        
        # Custom cake
        {"text": "Đặt bánh theo yêu cầu", "intent": "custom_cake"},
        {"text": "Làm bánh riêng được không?", "intent": "custom_cake"},
        
        # Ask feedback
        {"text": "Đánh giá của khách", "intent": "ask_feedback"},
        {"text": "Review bánh", "intent": "ask_feedback"},
        
        # Ask combo
        {"text": "Có combo nào không?", "intent": "ask_combo"},
        {"text": "Gợi ý combo", "intent": "ask_combo"},
        
        # Ask preservation
        {"text": "Bảo quản bánh thế nào?", "intent": "ask_preservation"},
        {"text": "Cách giữ bánh", "intent": "ask_preservation"},
        
        # Ask return
        {"text": "Đổi trả thế nào?", "intent": "ask_return"},
        {"text": "Chính sách hoàn trả", "intent": "ask_return"},
        
        # Ask new cake
        {"text": "Bánh mới nhất", "intent": "ask_new_cake"},
        {"text": "Có bánh gì mới không?", "intent": "ask_new_cake"},
        
        # Ask best seller
        {"text": "Bánh bán chạy nhất", "intent": "ask_best_seller"},
        {"text": "Bánh nào hot nhất?", "intent": "ask_best_seller"},
        
        # Ask for kids
        {"text": "Bánh cho trẻ em", "intent": "ask_for_kids"},
        {"text": "Bánh cho bé", "intent": "ask_for_kids"},
        
        # Ask nutrition
        {"text": "Thông tin dinh dưỡng", "intent": "ask_nutrition"},
        {"text": "Calo của bánh", "intent": "ask_nutrition"},
    ]
    
    training_data.extend(basic_intents)
    
    # Lưu vào file JSON
    output_file = "data/data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Đã đồng bộ {len(training_data)} mẫu training data vào {output_file}")
    print(f"📊 Thống kê:")
    print(f"   - Sản phẩm: {len(products)}")
    print(f"   - Danh mục: {len(categories)}")
    print(f"   - Khuyến mãi: {len(discounts)}")
    print(f"   - Tổng data: {len(training_data)} samples")
    print(f"\n💡 Bây giờ chạy: python train.py để train lại model với data mới!")
    
    store_client.close()

if __name__ == "__main__":
    print("=" * 60)
    print("🔄 ĐỒNG BỘ DATA TỪ WEB BÁN BÁNH")
    print("=" * 60)
    sync_data_from_web()
    print("=" * 60)
