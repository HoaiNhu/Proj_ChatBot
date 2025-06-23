# Chứa luật nhận diện intent và mapping intent sang response
INTENT_RULES = [
    {"keywords": ["bánh", "gợi ý", "vị"], "intent": "suggest_cake"},
    {"keywords": ["giá", "bao nhiêu", "tiền"], "intent": "ask_price"},
    {"keywords": ["nhân viên", "kết nối", "liên hệ"], "intent": "connect_staff"},
    # ... thêm luật khác
]

INTENT_RESPONSES = {
    "suggest_cake": [
        "Chúng tôi có nhiều loại bánh ngon. Bạn thích vị gì?",
        "Bạn muốn thử bánh vị nào? Socola, vani, trà xanh?"
    ],
    "ask_price": [
        "Bánh của chúng tôi có giá từ 200,000đ đến 2,000,000đ tùy loại.",
        "Bạn muốn hỏi giá loại bánh nào ạ?"
    ],
    "connect_staff": [
        "Bạn vui lòng đợi, nhân viên sẽ kết nối với bạn ngay.",
        "Chúng tôi sẽ chuyển bạn tới nhân viên hỗ trợ."
    ],
    # ... thêm intent khác
}