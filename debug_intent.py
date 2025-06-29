#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.conversation_service import ConversationService
from services.response_service import ResponseService
from logic.intent_rules import INTENT_RULES
from logic.intent_list import INTENT_LIST

def debug_intent_detection():
    """Debug logic detect intent"""
    print("=== DEBUG INTENT DETECTION ===")
    
    # Khởi tạo services
    conversation_service = ConversationService("models/")
    response_service = ResponseService()
    
    # Test cases
    test_cases = [
        "bánh dâu tây ngọt ngào",
        "giá bao nhiêu", 
        "Tiramisu 5 lớp giá bao nhiêu",
        "bánh kem socola nâu giá nhiêu",
        "còn bánh khác không"
    ]
    
    for i, message in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: '{message}' ---")
        
        # Test detect_intent_logic
        intent_logic, conf_logic = conversation_service.detect_intent_logic(message)
        print(f"Logic Intent: {intent_logic}, Confidence: {conf_logic}")
        
        # Test detect_intent (full)
        intent_full, conf_full = conversation_service.detect_intent(message)
        print(f"Full Intent: {intent_full}, Confidence: {conf_full}")
        
        # Test context rules
        context_intent = conversation_service.check_context_rules(message.lower())
        print(f"Context Intent: {context_intent}")
        
        # Test extract entities
        conversation_service.extract_entities(message)
        print(f"Current Context: {conversation_service.conversation_context}")
        
        # Test get_cake_name_from_message
        cake_name_from_message = conversation_service.get_cake_name_from_message(message)
        print(f"Cake name from message: {cake_name_from_message}")
        
        # Test context action với user_message
        context_action = conversation_service.get_context_action(intent_full, message)
        print(f"Context Action: {context_action}")
        
        # Test response
        if context_action:
            response = response_service.get_response(INTENT_LIST.index(intent_full) if intent_full in INTENT_LIST else 0, message, context_action)
        else:
            response = response_service.get_response(INTENT_LIST.index(intent_full) if intent_full in INTENT_LIST else 0, message)
        print(f"Response: {response}")
        
        print("-" * 50)

def debug_intent_rules():
    """Debug intent rules matching"""
    print("\n=== DEBUG INTENT RULES ===")
    
    test_cases = [
        "Tiramisu 5 lớp giá bao nhiêu",
        "bánh kem socola nâu giá nhiêu",
        "giá bao nhiêu"
    ]
    
    for message in test_cases:
        print(f"\nMessage: '{message}'")
        text_lower = message.lower()
        
        for rule in INTENT_RULES:
            if any(keyword in text_lower for keyword in rule["keywords"]):
                print(f"  Matched rule: {rule['intent']} with keywords: {rule['keywords']}")

if __name__ == "__main__":
    debug_intent_detection()
    debug_intent_rules() 