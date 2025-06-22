# Customer Support Chatbot

Hệ thống chatbot hỗ trợ khách hàng sử dụng NLP với Transformer, tích hợp Facebook Messenger và Zalo.

## Tính năng

✅ **NLP với Transformer (DistilBERT)**

- Hiểu ngôn ngữ tự nhiên tiếng Việt
- Xử lý từ viết tắt
- Dự đoán intent với confidence score

✅ **Tích hợp MongoDB**

- Lưu trữ cuộc trò chuyện
- Quản lý sản phẩm
- Thu thập phản hồi

✅ **Hệ thống học hỏi tự động**

- Thu thập dữ liệu từ cuộc trò chuyện
- Phân tích và tạo dữ liệu huấn luyện mới
- Huấn luyện lại mô hình tự động

✅ **Tích hợp Messenger**

- Facebook Messenger webhook
- Zalo webhook
- Gửi tin nhắn tự động

✅ **API đầy đủ**

- Chat API
- Feedback API
- Metrics API
- Health check
- Retrain API

✅ **Logging và Monitoring**

- Log chi tiết
- Số liệu hiệu suất
- Health monitoring

## Cài đặt

### Bước 1: Thiết lập môi trường

```bash
cd Proj1_Chatbot/chatbot
python -m venv venv
venv\Scripts\activate  # Windows
# hoặc
source venv/bin/activate  # Linux/Mac
```

### Bước 2: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Bước 3: Cấu hình môi trường

Tạo file `.env` từ `.env.example`:

```bash
# MongoDB Configuration
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority

# Facebook Messenger Configuration
FACEBOOK_PAGE_ACCESS_TOKEN=your_facebook_page_access_token
FACEBOOK_VERIFY_TOKEN=your_facebook_verify_token

# Zalo Configuration
ZALO_ACCESS_TOKEN=your_zalo_access_token
ZALO_VERIFY_TOKEN=your_zalo_verify_token

# Flask Configuration
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=chatbot.log
```

### Bước 4: Huấn luyện mô hình

```bash
python train.py
```

### Bước 5: Chạy ứng dụng

```bash
python chatbot.py
```

## Sử dụng Docker

### Build và chạy với Docker Compose

```bash
docker-compose up --build
```

### Hoặc chạy với Docker

```bash
docker build -t chatbot .
docker run -p 5005:5005 chatbot
```

## API Endpoints

### Chat API

```bash
POST /chat
{
  "message": "Bánh này giá bao nhiêu?"
}
```

### Feedback API

```bash
POST /feedback
{
  "user_input": "Bánh này giá bao nhiêu?",
  "bot_response": "Sản phẩm có giá 200,000 VND",
  "is_helpful": true,
  "feedback_text": "Rất hữu ích"
}
```

### Metrics API

```bash
GET /metrics?days=30
```

### Health Check

```bash
GET /health
```

### Retrain Model

```bash
POST /retrain
```

## Webhook Configuration

### Facebook Messenger

1. Tạo Facebook App
2. Cấu hình webhook URL: `https://your-domain.com/webhook`
3. Verify token: Sử dụng `FACEBOOK_VERIFY_TOKEN`

### Zalo

1. Tạo Zalo App
2. Cấu hình webhook URL: `https://your-domain.com/webhook`
3. Verify token: Sử dụng `ZALO_VERIFY_TOKEN`

## Cấu trúc dự án

```
chatbot/
├── chatbot.py              # Main application
├── config.py               # Configuration
├── logger.py               # Logging system
├── learning_system.py      # Learning system
├── messenger_integration.py # Messenger integration
├── train.py                # Training script
├── data.json               # Training data
├── abbreviations.txt       # Abbreviations
├── requirements.txt        # Dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker compose
└── logs/                  # Log files
```

## Monitoring

### Logs

Logs được lưu trong thư mục `logs/` với format:

- `chatbot_YYYYMMDD.log`

### Metrics

- Tổng số cuộc trò chuyện
- Tỷ lệ hài lòng
- Số phản hồi hữu ích/không hữu ích

## Troubleshooting

### Lỗi kết nối MongoDB

- Kiểm tra `MONGO_URI` trong file `.env`
- Đảm bảo IP được whitelist trong MongoDB Atlas

### Lỗi mô hình

- Chạy lại `python train.py`
- Kiểm tra file `trained_model/` tồn tại

### Lỗi webhook

- Kiểm tra verify token
- Đảm bảo URL webhook có thể truy cập từ internet
