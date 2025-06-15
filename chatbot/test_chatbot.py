#!/usr/bin/env python3
"""
Script test cho chatbot
"""

import requests
import json
import time

# URL của chatbot
BASE_URL = "http://localhost:5005"

def test_health():
    """Test health check"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_chat(message):
    """Test chat API"""
    print(f"💬 Testing chat with: '{message}'")
    try:
        response = requests.post(f"{BASE_URL}/chat", 
                               json={"message": message})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Bot response: {data['text']}")
            return data['text']
        else:
            print(f"❌ Chat failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return None

def test_feedback():
    """Test feedback API"""
    print("📝 Testing feedback API...")
    try:
        feedback_data = {
            "user_input": "Bánh này giá bao nhiêu?",
            "bot_response": "Sản phẩm có giá 200,000 VND",
            "is_helpful": True,
            "feedback_text": "Rất hữu ích"
        }
        response = requests.post(f"{BASE_URL}/feedback", json=feedback_data)
        if response.status_code == 200:
            print("✅ Feedback submitted successfully")
            return True
        else:
            print(f"❌ Feedback failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Feedback error: {e}")
        return False

def test_metrics():
    """Test metrics API"""
    print("📊 Testing metrics API...")
    try:
        response = requests.get(f"{BASE_URL}/metrics?days=7")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Metrics: {data}")
            return True
        else:
            print(f"❌ Metrics failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Metrics error: {e}")
        return False

def test_retrain():
    """Test retrain API"""
    print("🔄 Testing retrain API...")
    try:
        response = requests.post(f"{BASE_URL}/retrain")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrain: {data}")
            return True
        else:
            print(f"❌ Retrain failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Retrain error: {e}")
        return False

def main():
    """Chạy tất cả tests"""
    print("🚀 Starting chatbot tests...\n")
    
    # Test health check
    if not test_health():
        print("❌ Health check failed, stopping tests")
        return
    
    print()
    
    # Test chat với các câu khác nhau
    test_messages = [
        "Tôi muốn bánh ngọt",
        "Bánh này giá bao nhiêu?",
        "Tôi cần nói chuyện với nhân viên",
        "Gợi ý bánh nào ngon?",
        "Bánh socola giá sao vậy?"
    ]
    
    for message in test_messages:
        test_chat(message)
        print()
        time.sleep(1)  # Delay giữa các requests
    
    # Test feedback
    test_feedback()
    print()
    
    # Test metrics
    test_metrics()
    print()
    
    # Test retrain (optional)
    # test_retrain()
    # print()
    
    print("🎉 All tests completed!")

if __name__ == "__main__":
    main() 