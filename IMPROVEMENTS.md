# Cải tiến Chatbot - Context Management & Response Diversity

## Vấn đề ban đầu

Chatbot gặp các vấn đề sau:

1. **Luôn trả về cùng một bánh**: Chỉ gợi ý "Bánh hoa xuân" vì logic luôn lấy bánh có rating cao nhất
2. **Không hiểu context**: Không nhớ được thông tin từ các câu hỏi trước đó
3. **Trả lời không phù hợp**: Khi user hỏi "còn bánh khác không" thì vẫn trả về cùng bánh

## Các cải tiến đã thực hiện

### 1. Cải thiện Response Service (`services/response_service.py`)

#### a) Đa dạng hóa gợi ý bánh

- **Trước**: Luôn lấy bánh có `totalRatings` cao nhất
- **Sau**: Lấy 3-5 bánh ngẫu nhiên từ top 10 bánh có `averageRating` cao
- **Code**:

```python
# Lấy 3-5 bánh ngẫu nhiên từ top 10 bánh có rating cao
top_cakes = list(store_db['products'].find({}, {"productName": 1, "productPrice": 1, "averageRating": 1}).sort([("averageRating", -1)]).limit(10))
if top_cakes:
    import random
    selected_cakes = random.sample(top_cakes, min(3, len(top_cakes)))
```

#### b) Cải thiện hiển thị thông tin

- Thêm giá và rating vào gợi ý bánh
- Format giá với dấu phẩy ngăn cách hàng nghìn
- **Ví dụ**: "Bánh Hương Hoa Hồng (300,000đ, ⭐4)"

#### c) Xử lý fallback tốt hơn

- Thêm fallback response cho tất cả các intent
- Tránh trả về None hoặc lỗi

### 2. Thêm Context Management (`services/conversation_service.py`)

#### a) Lưu trữ context

- Lưu thông tin về câu hỏi và trả lời gần nhất
- Extract entities từ user message (tên bánh, số người, dịp lễ)
- Lưu lịch sử 5 câu gần nhất

#### b) Context Actions

- `combo_with_people`: Khi user hỏi combo sau khi đã nói số người
- `ingredient_after_suggest`: Khi user hỏi thành phần sau khi được gợi ý bánh
- `price_after_suggest`: Khi user hỏi giá sau khi được gợi ý bánh
- `suggest_more_cakes`: Khi user hỏi "còn bánh khác không"
- `combo_with_cake`: Khi user hỏi combo với bánh cụ thể

#### c) Entity Extraction

- Tự động nhận diện tên bánh trong câu hỏi
- Extract số lượng người (ví dụ: "5 người")
- Nhận diện dịp lễ (sinh nhật, cưới, tiệc, etc.)

### 3. Cập nhật Main API (`main.py`)

#### a) Sử dụng Conversation Service

- Thay thế logic context cũ bằng conversation service
- Tự động xóa context khi bắt đầu session mới

#### b) Thêm endpoint `/clear-context`

- Cho phép xóa context khi cần

### 4. Cải thiện Response Logic

#### a) Xử lý "còn bánh khác không"

```python
elif context_flag == "suggest_more_cakes":
    # Lấy 3 bánh khác ngẫu nhiên từ top 10
    top_cakes = list(store_db['products'].find({}, {"productName": 1, "productPrice": 1, "averageRating": 1}).sort([("averageRating", -1)]).limit(10))
    if len(top_cakes) >= 3:
        import random
        selected_cakes = random.sample(top_cakes, 3)
        # Trả về danh sách bánh khác
```

#### b) Xử lý combo với số người

```python
elif context_flag == "combo_with_people":
    people_count = context_action.get("people_count", 5)
    return f"Với {people_count} người, shop gợi ý combo bánh kem + bánh ngọt nhỏ, tổng giá khoảng 500.000đ. Bạn có muốn đặt không?"
```

## Kết quả mong đợi

### Trước khi cải tiến:

```
User: shop có combo nào vậy
Bot: Bạn cần combo cho bao nhiêu người? Shop sẽ gợi ý phù hợp nhé!

User: 5 người nhé
Bot: Shop đã chuyển thông tin của bạn cho nhân viên, bạn đợi chút nhé!

User: hôm nay có bánh nào ngon á
Bot: Shop gợi ý bạn thử bánh Bánh hoa xuân, vị rất được khách yêu thích!

User: còn bánh khác không
Bot: Bạn cần bánh cho tiệc sinh nhật? Shop gợi ý Bánh hoa xuân nhé!
```

### Sau khi cải tiến:

```
User: shop có combo nào vậy
Bot: Shop có thể tạo combo theo yêu cầu của bạn, bạn muốn combo gì ạ?

User: 5 người nhé
Bot: Với 5 người, shop gợi ý combo bánh kem + bánh ngọt nhỏ, tổng giá khoảng 500.000đ. Bạn có muốn đặt không?

User: hôm nay có bánh nào ngon á
Bot: Shop gợi ý bạn thử các loại bánh: Bánh Hương Hoa Hồng (300,000đ, ⭐4), Bánh Dâu Tây Ngọt Ngào (200,000đ, ⭐5), Bánh Trái Cây Nhiệt Đới (300,000đ, ⭐4.5). Bạn thích loại nào?

User: còn bánh khác không
Bot: Shop còn có các loại bánh khác: Bánh Giáng Sinh (150,000đ, ⭐4), Bánh Hương Hoa Hồng (300,000đ, ⭐4), Bánh Dâu Tây Ngọt Ngào (200,000đ, ⭐5). Bạn thích loại nào?
```

## Cách test

1. Chạy chatbot:

```bash
cd Proj1_Chatbot
python main.py
```

2. Chạy test script:

```bash
python test_chatbot.py
```

3. Test thủ công qua API:

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "gợi ý bánh cho tôi", "platform": "test"}'
```

## Lưu ý

- Context được lưu trong memory của conversation service
- Mỗi session mới sẽ xóa context cũ
- Có thể gọi `/clear-context` để xóa context thủ công
- Logic random selection đảm bảo đa dạng trong gợi ý bánh
