# Cải Thiện Chatbot - Giải Quyết Vấn Đề "Kém Thông Minh"

## Vấn Đề Đã Phát Hiện

Dựa trên ví dụ hội thoại của user, chatbot gặp các vấn đề sau:

1. **Context không được duy trì tốt**: Khi user hỏi "thành phần gì" sau khi đã nói về bánh kem mâm xôi, chatbot không nhớ context và hỏi lại "thành phần của loại bánh nào"

2. **Logic xử lý câu hỏi ngắn gọn chưa hoàn thiện**: Các câu như "giá bao nhiêu", "thành phần gì" không được xử lý đúng context

3. **Extract entities không ổn định**: Việc tìm tên bánh trong message và cập nhật context chưa nhất quán

## Các Cải Thiện Đã Thực Hiện

### 1. Cải Thiện Logic Context trong `conversation_service.py`

#### a) Cải thiện `check_context_rules()`

```python
def check_context_rules(self, text_lower):
    """Cải thiện logic kiểm tra context rules"""
    # Nếu có tên bánh mới trong message, cập nhật context trước
    self.has_different_cake_name(text_lower)

    # Kiểm tra xem có phải câu hỏi ngắn gọn không
    if not self.is_short_question(text_lower):
        return None

    # Nếu là câu hỏi ngắn gọn và có context, trả về intent tương ứng
    for rule in SHORT_QUESTION_RULES:
        if rule.get('requires_context', False):
            pattern_matches = 0
            for pattern_word in rule["pattern"]:
                if pattern_word in text_lower:
                    pattern_matches += 1

            # Nếu match được pattern và có context, trả về intent
            if pattern_matches > 0 and self.conversation_context.get('current_cake'):
                return rule["context_intent"]

    return None
```

#### b) Cải thiện `is_short_question()`

- Thêm nhiều pattern hơn để nhận diện câu hỏi ngắn gọn
- Bao gồm: "giá bao nhiêu", "thành phần gì", "vị gì", "còn khác", etc.

#### c) Cải thiện `get_context_action()`

- Ưu tiên tên bánh trong message hiện tại
- Xử lý context flag cho từng intent cụ thể

### 2. Cải Thiện Logic Response trong `response_service.py`

#### a) Thêm `is_short_question_with_context()`

```python
def is_short_question_with_context(self, intent_name, user_message, context_action):
    """Kiểm tra xem có phải câu hỏi ngắn gọn cần context không"""
    short_questions = ["ask_price", "ask_ingredient", "ask_combo", "ask_promotion"]
    return intent_name in short_questions and context_action and context_action.get('cake_name')
```

#### b) Thêm `handle_short_question_with_context()`

- Xử lý câu hỏi ngắn gọn với context đã có
- Trả về thông tin cụ thể về bánh đang được thảo luận

#### c) Thêm `get_fallback_response()`

- Trả về response fallback phù hợp cho từng intent
- Tránh trả lời chung chung

### 3. Cải Thiện Thứ Tự Xử Lý trong `main.py`

#### a) Thứ tự xử lý đúng:

1. Extract entities TRƯỚC khi detect intent
2. Detect intent với context mới nhất
3. Lấy context_action với context đã cập nhật
4. Generate response với context_action
5. Update context sau khi có response

#### b) Debug logging

- Thêm debug logs để theo dõi context và intent
- Dễ dàng debug khi có vấn đề

## Kết Quả Mong Đợi

Sau khi cải thiện, chatbot sẽ:

1. **Nhớ context tốt hơn**: Khi user hỏi "thành phần gì" sau khi đã nói về bánh kem mâm xôi, chatbot sẽ trả lời về thành phần của bánh kem mâm xôi

2. **Xử lý câu hỏi ngắn gọn thông minh hơn**: "giá bao nhiêu" sẽ được hiểu là hỏi giá của bánh đang thảo luận

3. **Trả lời cụ thể hơn**: Thay vì hỏi lại "bánh nào", chatbot sẽ trả lời trực tiếp về bánh đang được thảo luận

## Cách Test

Chạy file test để kiểm tra:

```bash
python test_improved_chatbot.py
```

## Ví Dụ Hội Thoại Mong Đợi

**Trước khi cải thiện:**

```
User: bánh kem mâm xôi giá nhiêu
Bot: Bánh kem mâm xôi có giá 499,000đ.

User: thành phần gì
Bot: Bạn muốn hỏi thành phần của loại bánh nào ạ?
```

**Sau khi cải thiện:**

```
User: bánh kem mâm xôi giá nhiêu
Bot: Bánh kem mâm xôi có giá 499,000đ.

User: thành phần gì
Bot: Thành phần bánh kem mâm xôi: Bột mì, đường, trứng, sữa tươi và các nguyên liệu tự nhiên khác.
```

## Lưu Ý

- Đảm bảo MongoDB có dữ liệu sản phẩm đầy đủ
- Context được duy trì trong session, sẽ reset khi tạo session mới
- Debug logs sẽ in ra console để theo dõi quá trình xử lý
