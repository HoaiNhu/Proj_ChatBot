"""
Script demo để test chatbot với Gemini
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("🤖 DEMO CHATBOT VỚI GEMINI AI")
print("=" * 60)

# Test 1: Kiểm tra Gemini service
print("\n1️⃣ Kiểm tra Gemini service...")
try:
    from services.gemini_service import get_gemini_service
    gemini = get_gemini_service()
    if gemini.enabled:
        print("   ✅ Gemini API đã được cấu hình")
    else:
        print("   ⚠️ Gemini API chưa được cấu hình (sẽ dùng response gốc)")
except Exception as e:
    print(f"   ❌ Lỗi: {e}")

# Test 2: Kiểm tra MongoDB connection
print("\n2️⃣ Kiểm tra kết nối MongoDB...")
try:
    from pymongo import MongoClient
    from config.config_chatbot import ChatbotConfig
    
    store_client = MongoClient(ChatbotConfig.STORE_MONGO_URI)
    store_db = store_client[ChatbotConfig.STORE_DB_NAME]
    
    # Test query
    product_count = store_db['products'].count_documents({})
    print(f"   ✅ Kết nối thành công! Có {product_count} sản phẩm trong database")
    
    store_client.close()
except Exception as e:
    print(f"   ❌ Lỗi: {e}")

# Test 3: Kiểm tra model
print("\n3️⃣ Kiểm tra model AI...")
try:
    from services.nlp_service import NLPService
    nlp = NLPService(model_path="./models")
    
    test_message = "Tôi muốn bánh ngọt"
    intent, confidence = nlp.predict_intent(test_message)
    print(f"   ✅ Model hoạt động! Test: '{test_message}'")
    print(f"      → Intent: {intent}, Confidence: {confidence:.2f}")
except Exception as e:
    print(f"   ⚠️ Model chưa được train: {e}")
    print("   💡 Chạy: python train.py để train model")

# Test 4: Test response với/không Gemini
print("\n4️⃣ Test response...")
try:
    from services.response_service import ResponseService
    response_service = ResponseService()
    
    test_message = "Bánh socola bao nhiêu tiền?"
    intent = "ask_price"
    
    response = response_service.get_response(
        intent=intent,
        user_message=test_message,
        context_action=None,
        last_bot_intent=None,
        conversation_context={}
    )
    
    print(f"   User: {test_message}")
    print(f"   Bot: {response}")
    
    if gemini.enabled:
        print("   💬 (Response đã được Gemini cải thiện)")
    else:
        print("   📝 (Response gốc, chưa dùng Gemini)")
    
except Exception as e:
    print(f"   ❌ Lỗi: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✅ DEMO HOÀN TẤT!")
print("=" * 60)

print("\n💡 HƯỚNG DẪN:")
print("1. Để cập nhật data mới: python sync_data_from_web.py")
print("2. Để train model: python train.py")
print("3. Để chạy chatbot: python main.py")
print("\n📖 Xem thêm: GEMINI_UPDATE_GUIDE.md")
