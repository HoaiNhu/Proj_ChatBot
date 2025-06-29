# Context rules cho intent transitions (intent hiện tại, intent bot trước đó, context_action)
INTENT_TRANSITION_RULES = [
    # Hỏi giá sau khi bot vừa gợi ý bánh
    ("ask_price", "suggest_cake", {"context_flag": "price_after_suggest"}),
    # Hỏi thành phần sau khi bot vừa gợi ý bánh
    ("ask_ingredient", "suggest_cake", {"context_flag": "ingredient_after_suggest"}),
    # Hỏi giá sau khi bot vừa hỏi khuyến mãi
    ("ask_price", "ask_promotion", {"context_flag": "promotion_price"}),
    # Hỏi thành phần sau khi hỏi khuyến mãi
    ("ask_ingredient", "ask_promotion", {"context_flag": "promotion_ingredient"}),
    # Hỏi khuyến mãi sau khi hỏi giá
    ("ask_promotion", "ask_price", {"context_flag": "promotion_after_price"}),
    # Hỏi combo sau khi hỏi khuyến mãi
    ("ask_combo", "ask_promotion", {"context_flag": "combo_after_promotion"}),
    # Hỏi giao hàng sau khi hỏi giá
    ("ask_delivery", "ask_price", {"context_flag": "delivery_after_price"}),
    # Hỏi giao hàng sau khi hỏi combo
    ("ask_delivery", "ask_combo", {"context_flag": "delivery_after_combo"}),
    # Hỏi feedback sau khi nhận hàng (check_order)
    ("ask_feedback", "check_order", {"context_flag": "feedback_after_order"}),
    # Hỏi thành phần sau khi hỏi giá
    ("ask_ingredient", "ask_price", {"context_flag": "ingredient_after_price"}),
    # Hỏi giá sau khi hỏi thành phần
    ("ask_price", "ask_ingredient", {"context_flag": "price_after_ingredient"}),
    # Hỏi khuyến mãi sau khi hỏi combo
    ("ask_promotion", "ask_combo", {"context_flag": "promotion_after_combo"}),
    # Hỏi combo sau khi hỏi giá
    ("ask_combo", "ask_price", {"context_flag": "combo_after_price"}),
    # Hỏi giao hàng sau khi hỏi khuyến mãi
    ("ask_delivery", "ask_promotion", {"context_flag": "delivery_after_promotion"}),
    # Hỏi feedback sau khi hỏi giao hàng
    ("ask_feedback", "ask_delivery", {"context_flag": "feedback_after_delivery"}),
    # Hỏi thành phần sau khi hỏi combo
    ("ask_ingredient", "ask_combo", {"context_flag": "ingredient_after_combo"}),
    # Hỏi giá sau khi hỏi giao hàng
    ("ask_price", "ask_delivery", {"context_flag": "price_after_delivery"}),
    # Hỏi khuyến mãi sau khi hỏi thành phần
    ("ask_promotion", "ask_ingredient", {"context_flag": "promotion_after_ingredient"}),
    # Hỏi combo sau khi hỏi thành phần
    ("ask_combo", "ask_ingredient", {"context_flag": "combo_after_ingredient"}),
    # Hỏi giao hàng sau khi hỏi thành phần
    ("ask_delivery", "ask_ingredient", {"context_flag": "delivery_after_ingredient"}),
    # Hỏi feedback sau khi hỏi combo
    ("ask_feedback", "ask_combo", {"context_flag": "feedback_after_combo"}),
    # Hỏi feedback sau khi hỏi khuyến mãi
    ("ask_feedback", "ask_promotion", {"context_flag": "feedback_after_promotion"}),
    # Hỏi feedback sau khi hỏi giá
    ("ask_feedback", "ask_price", {"context_flag": "feedback_after_price"}),
    # Hỏi feedback sau khi hỏi thành phần
    ("ask_feedback", "ask_ingredient", {"context_flag": "feedback_after_ingredient"}),
    # Hỏi feedback sau khi hỏi suggest_cake
    ("ask_feedback", "suggest_cake", {"context_flag": "feedback_after_suggest"}),
]

# Context rules cho câu hỏi ngắn gọn (pattern matching)
SHORT_QUESTION_RULES = [
    # Khi user hỏi "giá bao nhiêu" sau khi đã nói về bánh cụ thể
    {"pattern": ["giá", "bao nhiêu"], "context_intent": "ask_price", "requires_context": True},
    {"pattern": ["bao nhiêu", "tiền"], "context_intent": "ask_price", "requires_context": True},
    {"pattern": ["bao nhiêu", "đ"], "context_intent": "ask_price", "requires_context": True},
    {"pattern": ["chi phí", "bao nhiêu"], "context_intent": "ask_price", "requires_context": True},
    
    # Khi user hỏi về thành phần
    {"pattern": ["thành phần", "gì"], "context_intent": "ask_ingredient", "requires_context": True},
    {"pattern": ["làm từ", "gì"], "context_intent": "ask_ingredient", "requires_context": True},
    {"pattern": ["nguyên liệu", "gì"], "context_intent": "ask_ingredient", "requires_context": True},
    
    # Khi user hỏi về vị
    {"pattern": ["vị", "gì"], "context_intent": "ask_ingredient", "requires_context": True},
    {"pattern": ["hương vị", "gì"], "context_intent": "ask_ingredient", "requires_context": True},
    {"pattern": ["mùi vị", "gì"], "context_intent": "ask_ingredient", "requires_context": True},
    
    # Khi user hỏi về bánh khác
    {"pattern": ["còn", "khác"], "context_intent": "suggest_cake", "requires_context": True},
    {"pattern": ["bánh", "khác"], "context_intent": "suggest_cake", "requires_context": True},
    {"pattern": ["loại", "khác"], "context_intent": "suggest_cake", "requires_context": True},
    
    # Khi user hỏi về combo
    {"pattern": ["combo", "nào"], "context_intent": "ask_combo", "requires_context": True},
    {"pattern": ["gói", "nào"], "context_intent": "ask_combo", "requires_context": True},
    {"pattern": ["set", "nào"], "context_intent": "ask_combo", "requires_context": True},
    
    # Khi user hỏi về khuyến mãi
    {"pattern": ["khuyến mãi", "gì"], "context_intent": "ask_promotion", "requires_context": True},
    {"pattern": ["ưu đãi", "gì"], "context_intent": "ask_promotion", "requires_context": True},
    {"pattern": ["giảm giá", "gì"], "context_intent": "ask_promotion", "requires_context": True},
    
    # Khi user hỏi về giao hàng
    {"pattern": ["giao", "không"], "context_intent": "ask_delivery", "requires_context": True},
    {"pattern": ["ship", "không"], "context_intent": "ask_delivery", "requires_context": True},
    {"pattern": ["vận chuyển", "không"], "context_intent": "ask_delivery", "requires_context": True},
]

# Giữ lại CONTEXT_RULES cũ để tương thích ngược
CONTEXT_RULES = INTENT_TRANSITION_RULES + SHORT_QUESTION_RULES