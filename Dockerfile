FROM python:3.9-slim

# Cài đặt dependencies hệ thống
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Tạo thư mục làm việc
WORKDIR /app

# Copy requirements và cài đặt Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Tạo thư mục logs
RUN mkdir -p logs

# Expose port
EXPOSE 5005

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5005/health || exit 1

# Chạy ứng dụng
  CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]