#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_context_fix():
    """Test sửa lỗi context stuck"""
    base_url = "http://localhost:8000"
    
    print("=== TESTING CONTEXT FIX ===")
    print("Testing context management improvements...")
    print()
    
    # Tạo session_id để duy trì context
    session_id = None
    
    # Test 1: Hỏi về bánh đầu tiên
    print("1. Hỏi về bánh đầu tiên:")
    response1 = requests.post(f"{base_url}/chat", json={
        "message": "bánh dâu tây ngọt ngào",
        "session_id": session_id
    })
    result1 = response1.json()
    try:
        session_id = result1['session_id']  # Lưu session_id để dùng cho các request tiếp theo
        print(f"Session ID: {session_id}")
        print(f"User: bánh dâu tây ngọt ngào")
        print(f"Bot: {result1['text']}")
        print(f"Intent: {result1['intent']}")
    except KeyError as e:
        print(f"❌ Lỗi: {e}")
        print(f"Response đầy đủ: {result1}")
    print("-" * 50)
    
    # Test 2: Hỏi giá bánh đầu tiên
    print("2. Hỏi giá bánh đầu tiên:")
    response2 = requests.post(f"{base_url}/chat", json={
        "message": "giá bao nhiêu",
        "session_id": session_id
    })
    result2 = response2.json()
    print(f"Session ID: {session_id}")
    print(f"User: giá bao nhiêu")
    try:
        print(f"Bot: {result2['text']}")
        print(f"Intent: {result2['intent']}")
    except KeyError as e:
        print(f"❌ Lỗi: {e}")
        print(f"Response đầy đủ: {result2}")
    print("-" * 50)
    
    # Test 3: Hỏi về bánh mới (quan trọng!)
    print("3. Hỏi về bánh mới:")
    response3 = requests.post(f"{base_url}/chat", json={
        "message": "Tiramisu 5 lớp giá bao nhiêu",
        "session_id": session_id
    })
    result3 = response3.json()
    print(f"Session ID: {session_id}")
    print(f"User: Tiramisu 5 lớp giá bao nhiêu")
    print(f"Bot: {result3['text']}")
    print(f"Intent: {result3['intent']}")
    print("-" * 50)
    
    # Test 4: Hỏi giá ngắn gọn sau khi đã hỏi bánh mới
    print("4. Hỏi giá ngắn gọn sau bánh mới:")
    response4 = requests.post(f"{base_url}/chat", json={
        "message": "giá bao nhiêu",
        "session_id": session_id
    })
    result4 = response4.json()
    print(f"Session ID: {session_id}")
    print(f"User: giá bao nhiêu")
    print(f"Bot: {result4['text']}")
    print(f"Intent: {result4['intent']}")
    print("-" * 50)
    
    # Test 5: Hỏi bánh khác
    print("5. Hỏi bánh khác:")
    response5 = requests.post(f"{base_url}/chat", json={
        "message": "bánh kem socola nâu giá nhiêu",
        "session_id": session_id
    })
    result5 = response5.json()
    print(f"Session ID: {session_id}")
    print(f"User: bánh kem socola nâu giá nhiêu")
    print(f"Bot: {result5['text']}")
    print(f"Intent: {result5['intent']}")
    print("-" * 50)
    
    # Test 6: Hỏi còn bánh khác không
    print("6. Hỏi còn bánh khác không:")
    response6 = requests.post(f"{base_url}/chat", json={
        "message": "còn bánh khác không",
        "session_id": session_id
    })
    result6 = response6.json()
    print(f"Session ID: {session_id}")
    print(f"User: còn bánh khác không")
    print(f"Bot: {result6['text']}")
    print(f"Intent: {result6['intent']}")
    print("-" * 50)
    
    print("=== CONTEXT FIX TEST COMPLETED ===")

if __name__ == "__main__":
    try:
        test_context_fix()
    except requests.exceptions.ConnectionError:
        print("❌ Không thể kết nối đến chatbot server")
        print("Hãy đảm bảo server đang chạy trên http://localhost:8000")
    except Exception as e:
        print(f"❌ Lỗi: {e}") 