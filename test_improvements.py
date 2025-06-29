#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_chatbot_improvements():
    """Test các cải thiện của chatbot"""
    base_url = "http://localhost:8000"
    
    print("=== TESTING CHATBOT IMPROVEMENTS ===")
    print("Testing context understanding and short questions...")
    print()
    
    # Test 1: Hỏi về bánh cụ thể
    print("1. Hỏi về bánh cụ thể:")
    response1 = requests.post(f"{base_url}/chat", json={
        "message": "bánh dâu tây ngọt ngào"
    })
    result1 = response1.json()
    print(f"User: bánh dâu tây ngọt ngào")
    print(f"Bot: {result1['response']}")
    print(f"Intent: {result1['intent']}")
    print(f"Confidence: {result1['confidence']:.2f}")
    print("-" * 50)
    
    # Test 2: Hỏi giá ngắn gọn (không nhắc tên bánh)
    print("2. Hỏi giá ngắn gọn:")
    response2 = requests.post(f"{base_url}/chat", json={
        "message": "giá bao nhiêu"
    })
    result2 = response2.json()
    print(f"User: giá bao nhiêu")
    print(f"Bot: {result2['response']}")
    print(f"Intent: {result2['intent']}")
    print(f"Confidence: {result2['confidence']:.2f}")
    print("-" * 50)
    
    # Test 3: Hỏi thành phần ngắn gọn
    print("3. Hỏi thành phần ngắn gọn:")
    response3 = requests.post(f"{base_url}/chat", json={
        "message": "thành phần gì"
    })
    result3 = response3.json()
    print(f"User: thành phần gì")
    print(f"Bot: {result3['response']}")
    print(f"Intent: {result3['intent']}")
    print(f"Confidence: {result3['confidence']:.2f}")
    print("-" * 50)
    
    # Test 4: Hỏi vị ngắn gọn
    print("4. Hỏi vị ngắn gọn:")
    response4 = requests.post(f"{base_url}/chat", json={
        "message": "vị gì"
    })
    result4 = response4.json()
    print(f"User: vị gì")
    print(f"Bot: {result4['response']}")
    print(f"Intent: {result4['intent']}")
    print(f"Confidence: {result4['confidence']:.2f}")
    print("-" * 50)
    
    # Test 5: Hỏi combo ngắn gọn
    print("5. Hỏi combo ngắn gọn:")
    response5 = requests.post(f"{base_url}/chat", json={
        "message": "combo nào"
    })
    result5 = response5.json()
    print(f"User: combo nào")
    print(f"Bot: {result5['response']}")
    print(f"Intent: {result5['intent']}")
    print(f"Confidence: {result5['confidence']:.2f}")
    print("-" * 50)
    
    # Test 6: Hỏi bánh khác
    print("6. Hỏi bánh khác:")
    response6 = requests.post(f"{base_url}/chat", json={
        "message": "còn bánh khác không"
    })
    result6 = response6.json()
    print(f"User: còn bánh khác không")
    print(f"Bot: {result6['response']}")
    print(f"Intent: {result6['intent']}")
    print(f"Confidence: {result6['confidence']:.2f}")
    print("-" * 50)
    
    # Test 7: Hỏi giá với từ khóa mới
    print("7. Hỏi giá với từ khóa mới:")
    response7 = requests.post(f"{base_url}/chat", json={
        "message": "bao nhiêu tiền"
    })
    result7 = response7.json()
    print(f"User: bao nhiêu tiền")
    print(f"Bot: {result7['response']}")
    print(f"Intent: {result7['intent']}")
    print(f"Confidence: {result7['confidence']:.2f}")
    print("-" * 50)
    
    # Test 8: Hỏi giá với từ khóa mới khác
    print("8. Hỏi giá với từ khóa mới khác:")
    response8 = requests.post(f"{base_url}/chat", json={
        "message": "chi phí bao nhiêu"
    })
    result8 = response8.json()
    print(f"User: chi phí bao nhiêu")
    print(f"Bot: {result8['response']}")
    print(f"Intent: {result8['intent']}")
    print(f"Confidence: {result8['confidence']:.2f}")
    print("-" * 50)
    
    print("=== IMPROVEMENTS TEST COMPLETED ===")

if __name__ == "__main__":
    try:
        test_chatbot_improvements()
    except requests.exceptions.ConnectionError:
        print("❌ Không thể kết nối đến chatbot server")
        print("Hãy đảm bảo server đang chạy trên http://localhost:8000")
    except Exception as e:
        print(f"❌ Lỗi: {e}") 