#!/usr/bin/env python3
"""
Test script để kiểm tra chatbot với các câu hỏi mẫu
"""

import requests
import json
import time

# URL của chatbot API
BASE_URL = "http://localhost:8000"

def test_chat(message, session_id=None):
    """Test gửi tin nhắn đến chatbot"""
    url = f"{BASE_URL}/chat"
    data = {
        "message": message,
        "session_id": session_id,
        "platform": "test"
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"User: {message}")
            print(f"Bot: {result['text']}")
            print(f"Intent: {result['intent']}")
            print(f"Confidence: {result['confidence']:.2f}")
            print("-" * 50)
            return result
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def test_conversation_flow():
    """Test luồng hội thoại mẫu"""
    print("=== TESTING CHATBOT CONVERSATION FLOW ===")
    
    # Test 1: Hỏi về combo
    print("\n1. Hỏi về combo:")
    result1 = test_chat("shop có combo nào vậy")
    
    # Test 2: Trả lời số người
    print("\n2. Trả lời số người:")
    result2 = test_chat("5 người nhé", result1['session_id'] if result1 else None)
    
    # Test 3: Hỏi bánh ngon
    print("\n3. Hỏi bánh ngon:")
    result3 = test_chat("hôm nay có bánh nào ngon á")
    
    # Test 4: Hỏi bánh khác
    print("\n4. Hỏi bánh khác:")
    result4 = test_chat("còn bánh khác không", result3['session_id'] if result3 else None)
    
    # Test 5: Hỏi thành phần bánh cụ thể
    print("\n5. Hỏi thành phần bánh cụ thể:")
    result5 = test_chat("bánh hoa xuân có thành phần và vị như nào á", result4['session_id'] if result4 else None)
    
    # Test 6: Hỏi vị bánh
    print("\n6. Hỏi vị bánh:")
    result6 = test_chat("bánh hoa xuân vị gì á", result5['session_id'] if result5 else None)
    
    # Test 7: Hỏi combo khuyến mãi
    print("\n7. Hỏi combo khuyến mãi:")
    result7 = test_chat("combo nào đang được khuyến mãi á", result6['session_id'] if result6 else None)
    
    # Test 8: Hỏi lại combo
    print("\n8. Hỏi lại combo:")
    result8 = test_chat("shop có các combo nào vậy", result7['session_id'] if result7 else None)

def test_suggest_cakes():
    """Test gợi ý bánh nhiều lần để xem có đa dạng không"""
    print("\n=== TESTING CAKE SUGGESTIONS ===")
    
    session_id = None
    for i in range(5):
        print(f"\n--- Lần {i+1} ---")
        result = test_chat("gợi ý bánh cho tôi", session_id)
        if result:
            session_id = result['session_id']
        time.sleep(1)  # Đợi 1 giây giữa các request

def test_context_understanding():
    """Test khả năng hiểu context"""
    print("\n=== TESTING CONTEXT UNDERSTANDING ===")
    
    session_id = None
    
    # Test 1: Hỏi về bánh cụ thể
    print("\n1. Hỏi về bánh cụ thể:")
    result1 = test_chat("bánh dâu tây ngọt ngào", session_id)
    session_id = result1['session_id'] if result1 else None
    
    # Test 2: Hỏi giá bánh đó (không cần nhắc lại tên)
    print("\n2. Hỏi giá (không nhắc tên):")
    result2 = test_chat("giá bao nhiêu", session_id)
    
    # Test 3: Hỏi thành phần bánh đó
    print("\n3. Hỏi thành phần (không nhắc tên):")
    result3 = test_chat("thành phần gì", session_id)

def clear_context():
    """Xóa context"""
    try:
        response = requests.post(f"{BASE_URL}/clear-context")
        if response.status_code == 200:
            print("Context cleared successfully")
        else:
            print(f"Error clearing context: {response.status_code}")
    except Exception as e:
        print(f"Exception clearing context: {e}")

if __name__ == "__main__":
    print("Starting chatbot tests...")
    
    # Test health check
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Chatbot is running and healthy")
        else:
            print("❌ Chatbot is not healthy")
            exit(1)
    except Exception as e:
        print(f"❌ Cannot connect to chatbot: {e}")
        exit(1)
    
    # Chạy các test
    test_conversation_flow()
    test_suggest_cakes()
    test_context_understanding()
    
    print("\n=== TESTS COMPLETED ===") 