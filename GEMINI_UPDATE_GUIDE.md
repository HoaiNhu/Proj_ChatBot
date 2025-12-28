# 🤖 HƯỚNG DẪN CẬP NHẬT CHATBOT VỚI DATA MỚI VÀ GEMINI AI

## ❗ VẤN ĐỀ ĐÃ GIẢI QUYẾT

### 1. **Chatbot dùng data cũ sau khi update web**

**Nguyên nhân**:

- Chatbot lấy data **ĐỘNG** từ MongoDB web (đã đúng) ✅
- Nhưng **model AI chỉ hiểu intents cũ** vì được train với file `data/data.json` cũ ❌

**Giải pháp**:

- Tạo script `sync_data_from_web.py` để tự động đồng bộ data mới từ MongoDB web → `data.json`
- Train lại model với data mới

### 2. **Response chatbot cứng nhắc, không tự nhiên**

**Giải pháp**:

- Tích hợp **Google Gemini AI** để làm mượt câu trả lời
- Response sẽ tự nhiên hơn, có emoji, thân thiện hơn

---

## 🚀 HƯỚNG DẪN SỬ DỤNG

### Bước 1: Cài đặt thư viện mới

```bash
pip install google-generativeai
```

Hoặc cài tất cả:

```bash
pip install -r requirements.txt
```

### Bước 2: Lấy Gemini API Key (MIỄN PHÍ)

1. Truy cập: https://makersuite.google.com/app/apikey
2. Đăng nhập Google
3. Click "Create API Key"
4. Copy API key

### Bước 3: Cấu hình API Key

Mở file `.env` và thêm:

```env
GEMINI_API_KEY=your_api_key_here_paste_từ_bước_2
```

### Bước 4: Đồng bộ data mới từ web

**Chạy script này MỖI KHI update data trên web:**

```bash
python sync_data_from_web.py
```

Script này sẽ:

- ✅ Lấy tất cả sản phẩm mới từ MongoDB web
- ✅ Lấy categories mới
- ✅ Lấy khuyến mãi mới
- ✅ Tạo training data tự động
- ✅ Cập nhật file `data/data.json`

### Bước 5: Train lại model với data mới

```bash
python train.py
```

⏱️ Mất khoảng 5-10 phút tùy số lượng data

### Bước 6: Chạy chatbot

```bash
python main.py
```

Hoặc với uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8002
```

---

## 📋 QUY TRÌNH CẬP NHẬT DATA

**MỖI KHI thêm/sửa/xóa sản phẩm trên web:**

```bash
# 1. Đồng bộ data mới
python sync_data_from_web.py

# 2. Train lại model
python train.py

# 3. Restart chatbot
# Ctrl+C để stop
python main.py
```

---

## 🎯 TÍNH NĂNG MỚI

### 1. **Gemini AI Enhancement**

- ✨ Response tự nhiên hơn
- 😊 Có emoji phù hợp
- 💬 Giọng điệu thân thiện
- 🔄 Tự động viết lại câu trả lời

**Ví dụ:**

**Trước (không có Gemini):**

```
User: Bánh socola bao nhiêu tiền?
Bot: Bánh Chocolate Cake có giá 250,000đ.
```

**Sau (có Gemini):**

```
User: Bánh socola bao nhiêu tiền?
Bot: Bánh Chocolate Cake của shop giá 250,000đ nha bạn 🍰
     Bánh này đang rất được ưa chuộng đó! Bạn muốn đặt không? 😊
```

### 2. **Auto Sync Data**

- 🔄 Script tự động lấy data mới từ web
- 📊 Tạo training data từ:
  - Tên sản phẩm
  - Categories
  - Khuyến mãi
  - Các intent cơ bản

---

## ⚙️ CẤU HÌNH NÂNG CAO

### Tắt Gemini AI (nếu không muốn dùng)

Trong file `.env`, xóa hoặc comment dòng:

```env
# GEMINI_API_KEY=your_key_here
```

Chatbot sẽ tự động dùng response gốc nếu không có Gemini API key.

### Điều chỉnh Gemini prompt

Mở file `services/gemini_service.py` và chỉnh sửa hàm `_create_enhancement_prompt()` để thay đổi cách Gemini viết lại câu trả lời.

---

## 🐛 TROUBLESHOOTING

### Lỗi: "GEMINI_API_KEY not found"

→ Kiểm tra file `.env` đã có `GEMINI_API_KEY=...` chưa

### Chatbot vẫn dùng data cũ

→ Chạy lại:

```bash
python sync_data_from_web.py
python train.py
```

### Gemini response quá dài

→ Đã giới hạn 500 ký tự trong code, nếu vẫn dài có thể giảm xuống trong `gemini_service.py`

### Lỗi khi train model

→ Kiểm tra xem file `data/data.json` đã được tạo chưa bằng lệnh:

```bash
python sync_data_from_web.py
```

---

## 📁 FILES MỚI ĐƯỢC TẠO

1. **`sync_data_from_web.py`** - Script đồng bộ data từ MongoDB
2. **`services/gemini_service.py`** - Service tích hợp Gemini AI
3. **`GEMINI_UPDATE_GUIDE.md`** - File hướng dẫn này

---

## 💡 TIPS

1. **Đồng bộ data thường xuyên**: Nên setup cron job để chạy `sync_data_from_web.py` mỗi ngày
2. **Monitor Gemini usage**: API miễn phí có giới hạn 60 requests/phút
3. **Backup model**: Trước khi train lại, có thể backup folder `models/` để rollback nếu cần

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề, kiểm tra:

1. File `.env` đã cấu hình đúng
2. MongoDB đang hoạt động
3. Internet connection (để gọi Gemini API)
4. Log errors trong terminal

---

**Chúc bạn thành công! 🎉**
