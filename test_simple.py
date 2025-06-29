#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.response_service import ResponseService

def test_response_service():
    """Test response service với context_action"""
    print("=== TESTING RESPONSE SERVICE ===")
    
    response_service = ResponseService()
    
    # Test 1: Context action với Tiramisu 5 lớp
    print("\n1. Test context action với Tiramisu 5 lớp:")
    context_action = {
        'context_flag': 'price_after_suggest',
        'cake_name': 'Tiramisu 5 lớp'
    }
    response = response_service.get_response(4, "Tiramisu 5 lớp giá bao nhiêu", context_action)
    print(f"Context Action: {context_action}")
    print(f"Response: {response}")
    
    # Test 2: Context action với Bánh kem socola nâu
    print("\n2. Test context action với Bánh kem socola nâu:")
    context_action = {
        'context_flag': 'price_after_suggest',
        'cake_name': 'Bánh kem socola nâu'
    }
    response = response_service.get_response(4, "bánh kem socola nâu giá nhiêu", context_action)
    print(f"Context Action: {context_action}")
    print(f"Response: {response}")
    
    # Test 3: Context action với Bánh Dâu Tây Ngọt Ngào
    print("\n3. Test context action với Bánh Dâu Tây Ngọt Ngào:")
    context_action = {
        'context_flag': 'price_after_suggest',
        'cake_name': 'Bánh Dâu Tây Ngọt Ngào'
    }
    response = response_service.get_response(4, "giá bao nhiêu", context_action)
    print(f"Context Action: {context_action}")
    print(f"Response: {response}")

if __name__ == "__main__":
    test_response_service() 