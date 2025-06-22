# Chatbot FastAPI - Hệ thống hỗ trợ khách hàng

FastAPI backend cho hệ thống chatbot hỗ trợ khách hàng với tích hợp MongoDB và Facebook Messenger.

## 🚀 Tính năng

- **FastAPI**: API hiện đại với auto-documentation
- **MongoDB riêng biệt**: Tách biệt với MongoDB training
- **Facebook Messenger**: Webhook integration
- **Auto-docs**: Swagger UI tại `/docs`
- **Async support**: Xử lý bất đồng bộ hiệu quả
- **Pydantic validation**: Validate input tự động

## 📋 Yêu cầu hệ thống

- Python 3.8+
- MongoDB Atlas (riêng biệt)
- FastAPI + Uvicorn

## 🛠️ Cài đặt

1. **Clone và cài đặt dependencies**

```bash
cd Proj1_Chatbot/chatbot
pip install -r requirements.txt
```

2. **Cấu hình MongoDB riêng biệt**

```bash
# Tạo cluster MongoDB Atlas mới cho chatbot
# Copy connection string vào env.chatbot
cp env.chatbot .env
# Chỉnh sửa .env với thông tin thực tế
```

3. **Cấu hình Facebook Messenger** (tùy chọn)

```bash
# Thêm Facebook App ID và Secret vào .env
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret
FACEBOOK_VERIFY_TOKEN=your_verify_token
```

## 🚀 Chạy ứng dụng

### Development

```bash
python main.py
```

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Server sẽ chạy trên `http://localhost:8000`

## 📡 API Endpoints

### Core APIs

| Method | Endpoint            | Mô tả                  |
| ------ | ------------------- | ---------------------- |
| GET    | `/`                 | Root endpoint          |
| GET    | `/health`           | Health check           |
| POST   | `/chat`             | Xử lý tin nhắn         |
| GET    | `/products`         | Lấy danh sách sản phẩm |
| POST   | `/products/search`  | Tìm kiếm sản phẩm      |
| POST   | `/products/suggest` | Gợi ý sản phẩm         |
| POST   | `/feedback`         | Gửi đánh giá           |
| GET    | `/metrics`          | Thống kê               |
| POST   | `/retrain`          | Retrain model          |

### Facebook Messenger

| Method | Endpoint            | Mô tả            |
| ------ | ------------------- | ---------------- |
| POST   | `/webhook/facebook` | Facebook webhook |

### Auto-documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔧 Cấu hình MongoDB

### Tạo cluster riêng biệt

1. **Tạo MongoDB Atlas cluster mới**

   - Đăng ký tại [MongoDB Atlas](https://cloud.mongodb.com)
   - Tạo cluster mới với tên `chatbot-support`
   - Chọn region gần nhất

2. **Cấu hình Network Access**

   - Allow access from anywhere (0.0.0.0/0)
   - Hoặc chỉ cho phép IP cụ thể

3. **Tạo Database User**

   - Username: `chatbot_user`
   - Password: `secure_password`
   - Role: `Read and write to any database`

4. **Lấy Connection String**

```
mongodb+srv://chatbot_user:secure_password@cluster.mongodb.net/chatbot_support
```

### Collections trong chatbot database

```javascript
// conversations - Lưu thông tin cuộc trò chuyện
{
  session_id: String,
  user_id: String,
  platform: String,
  status: String,
  created_at: Date,
  updated_at: Date
}

// messages - Lưu từng tin nhắn
{
  session_id: String,
  sender: String, // user, bot, agent
  message: String,
  intent: Number,
  confidence: Number,
  timestamp: Date
}

// feedback - Lưu đánh giá
{
  session_id: String,
  rating: Number,
  comment: String,
  timestamp: Date
}

// users - Thông tin người dùng
{
  user_id: String,
  platform: String,
  first_seen: Date,
  last_seen: Date,
  total_conversations: Number
}

// analytics - Thống kê
{
  date: Date,
  total_conversations: Number,
  total_messages: Number,
  avg_rating: Number,
  popular_intents: Array
}
```

## 🚀 Deployment trên Render

1. **Push code lên GitHub**

```bash
git add .
git commit -m "Add FastAPI chatbot"
git push origin main
```

2. **Deploy trên Render**

- Tạo account tại [Render](https://render.com)
- Connect với GitHub repository
- Chọn `Web Service`
- Cấu hình:
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Cấu hình Environment Variables**

- `CHATBOT_MONGO_URI`: MongoDB connection string
- `FACEBOOK_APP_ID`: Facebook App ID
- `FACEBOOK_APP_SECRET`: Facebook App Secret
- `FACEBOOK_VERIFY_TOKEN`: Webhook verify token
- `JWT_SECRET`: Secret key cho JWT

## 🔌 Tích hợp với Node.js Backend

Node.js backend sẽ gọi FastAPI:

```javascript
// Trong ChatbotService.js
const CHATBOT_API_URL = "https://your-fastapi-app.onrender.com/chat";

export const sendMessage = async (message, sessionId) => {
  const response = await fetch(CHATBOT_API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
      session_id: sessionId,
      platform: "web",
    }),
  });

  return await response.json();
};
```

## 📊 Monitoring

### Health Check

```bash
curl https://your-app.onrender.com/health
```

### Metrics

```bash
curl https://your-app.onrender.com/metrics
```

### Swagger Documentation

```
https://your-app.onrender.com/docs
```

## 🔒 Bảo mật

- **CORS**: Cấu hình origins cụ thể
- **Rate Limiting**: Giới hạn requests
- **Input Validation**: Pydantic models
- **Environment Variables**: Không hardcode secrets

## 🆘 Troubleshooting

### Lỗi MongoDB connection

```bash
# Kiểm tra connection string
# Đảm bảo IP được whitelist
# Kiểm tra username/password
```

### Lỗi Facebook webhook

```bash
# Verify token phải khớp
# Webhook URL phải public
# SSL certificate required
```

### Lỗi model loading

```bash
# Kiểm tra MODEL_PATH
# Đảm bảo model files tồn tại
# Fallback to distilbert-base-uncased
```

## 📝 License

MIT License
