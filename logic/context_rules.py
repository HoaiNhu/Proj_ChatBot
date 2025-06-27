# (intent hiện tại, intent bot trước đó, context_action)
CONTEXT_RULES = [
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
    # ... có thể bổ sung thêm các rule context khác nếu cần ...
]