#!/usr/bin/env python3
"""
Test script để kiểm tra chatbot đã cải thiện chưa
"""

import requests
import json
import time

# URL của chatbot API
BASE_URL = "http://localhost:8000"

def test_chatbot_conversation():
    """Test cuộc hội thoại với chatbot"""
    
    # Test cases dựa trên ví dụ của user
    test_cases = [
        "hi",
        "bánh kem mâm xôi giá nhiêu", 
        "thành phần gì",
        "bánh kem socola nâu",
        "giá bao nhiêu",
        "bánh dâu tây ngọt ngào",
        "giá bao nhiêu"
    ]
    
    session_id = None
    
    print("=== TESTING IMPROVED CHATBOT ===")
    print("=" * 50)
    
    for i, message in enumerate(test_cases, 1):
        print(f"\n{i}. User: {message}")
        
        # Gửi request đến chatbot
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": message,
                "session_id": session_id,
                "platform": "test"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            bot_response = data.get("text", "")
            intent = data.get("intent", "")
            confidence = data.get("confidence", 0)
            session_id = data.get("session_id", session_id)
            
            print(f"   Bot: {bot_response}")
            print(f"   Intent: {intent}, Confidence: {confidence:.2f}")
        else:
            print(f"   Error: {response.status_code} - {response.text}")
        
        time.sleep(0.5)  # Delay nhỏ giữa các message
    
    print("\n" + "=" * 50)
    print("Test completed!")

def test_short_questions():
    """Test các câu hỏi ngắn gọn"""
    
    print("\n=== TESTING SHORT QUESTIONS ===")
    print("=" * 50)
    
    # Test với context về bánh kem mâm xôi
    test_sequence = [
        "bánh kem mâm xôi",
        "giá bao nhiêu",
        "thành phần gì", 
        "có khuyến mãi không"
    ]
    
    session_id = None
    
    for i, message in enumerate(test_sequence, 1):
        print(f"\n{i}. User: {message}")
        
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": message,
                "session_id": session_id,
                "platform": "test"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            bot_response = data.get("text", "")
            intent = data.get("intent", "")
            confidence = data.get("confidence", 0)
            session_id = data.get("session_id", session_id)
            
            print(f"   Bot: {bot_response}")
            print(f"   Intent: {intent}, Confidence: {confidence:.2f}")
        else:
            print(f"   Error: {response.status_code} - {response.text}")
        
        time.sleep(0.5)

def test_special_cases():
    """Test các trường hợp đặc biệt giống đoạn chat thực tế"""
    print("\n=== TESTING SPECIAL CASES ===")
    print("=" * 50)
    test_sequence = [
        "lô",
        "hello",
        "có bánh nào giá dưới 200k không",
        "bánh kem",
        "giá bánh nào dưới 200000",
        "bảo quản bánh thế nào",
        "có",
        "m dở á",
        "tôi muốn gặp nhân viên",
        "ok"
    ]
    session_id = None
    for i, message in enumerate(test_sequence, 1):
        print(f"\n{i}. User: {message}")
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": message,
                "session_id": session_id,
                "platform": "test"
            }
        )
        if response.status_code == 200:
            data = response.json()
            bot_response = data.get("text", "")
            intent = data.get("intent", "")
            confidence = data.get("confidence", 0)
            session_id = data.get("session_id", session_id)
            print(f"   Bot: {bot_response}")
            print(f"   Intent: {intent}, Confidence: {confidence:.2f}")
        else:
            print(f"   Error: {response.status_code} - {response.text}")
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        # Test 1: Cuộc hội thoại tổng quát
        test_chatbot_conversation()
        
        # Test 2: Câu hỏi ngắn gọn với context
        test_short_questions()
        
        # Test 3: Các trường hợp đặc biệt
        test_special_cases()
        
    except requests.exceptions.ConnectionError:
        print("Error: Không thể kết nối đến chatbot API.")
        print("Hãy đảm bảo server đang chạy trên localhost:8000")
    except Exception as e:
        print(f"Error: {e}") 