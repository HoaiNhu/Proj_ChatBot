from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import os
from datetime import datetime
import uuid

# Import các module hiện có
from chatbot import get_response, predict_intent, get_product_info, suggest_products
from config import Config
from logger import logger
from learning_system import LearningSystem
from messenger_integration import MessengerIntegration

# Khởi tạo FastAPI app
app = FastAPI(
    title="Chatbot Support API",
    description="API cho hệ thống chatbot hỗ trợ khách hàng",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production, chỉ cho phép domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    platform: str = "web"

class ChatResponse(BaseModel):
    text: str
    session_id: str
    intent: int
    confidence: float
    quick_replies: Optional[List[str]] = None
    attachments: Optional[List[Dict[str, Any]]] = None

class FeedbackRequest(BaseModel):
    session_id: str
    rating: int
    comment: Optional[str] = None

class ProductRequest(BaseModel):
    product_name: str

class RetrainRequest(BaseModel):
    force: bool = False

# Khởi tạo các hệ thống
learning_system = LearningSystem(None)  # Sẽ được cập nhật sau
messenger_integration = MessengerIntegration()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Chatbot Support API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Kiểm tra kết nối MongoDB
        from pymongo import MongoClient
        client = MongoClient(Config.MONGO_URI)
        client.admin.command('ping')
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "mongodb": "connected",
            "model": "loaded"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Xử lý tin nhắn từ người dùng"""
    try:
        # Tạo session_id nếu chưa có
        session_id = request.session_id or str(uuid.uuid4())
        
        # Xử lý tin nhắn
        response_text = get_response(
            user_input=request.message,
            platform=request.platform,
            user_id=request.user_id,
            session_id=session_id
        )
        
        # Lấy intent và confidence
        intent, confidence = predict_intent(request.message)
        
        # Tạo quick replies dựa trên intent
        quick_replies = generate_quick_replies(intent, request.message)
        
        return ChatResponse(
            text=response_text,
            session_id=session_id,
            intent=intent,
            confidence=confidence,
            quick_replies=quick_replies
        )
        
    except Exception as e:
        logger.error(f"Error processing chat: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/products")
async def get_products():
    """Lấy danh sách sản phẩm"""
    try:
        from pymongo import MongoClient
        client = MongoClient(Config.MONGO_URI)
        db = client['test']
        
        products = list(db['products'].find({}, {'_id': 0}).limit(20))
        return {"products": products}
        
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        raise HTTPException(status_code=500, detail="Error fetching products")

@app.post("/products/search")
async def search_products(request: ProductRequest):
    """Tìm kiếm sản phẩm"""
    try:
        product_info = get_product_info(request.product_name)
        if product_info:
            return {"product": product_info}
        else:
            return {"product": None, "message": "Product not found"}
            
    except Exception as e:
        logger.error(f"Error searching product: {e}")
        raise HTTPException(status_code=500, detail="Error searching product")

@app.post("/products/suggest")
async def suggest_products_endpoint(request: ChatRequest):
    """Gợi ý sản phẩm"""
    try:
        products = suggest_products(request.message)
        return {"suggestions": products}
        
    except Exception as e:
        logger.error(f"Error suggesting products: {e}")
        raise HTTPException(status_code=500, detail="Error suggesting products")

@app.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    """Gửi đánh giá từ khách hàng"""
    try:
        if not 1 <= request.rating <= 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        
        # Lưu feedback vào database
        from pymongo import MongoClient
        client = MongoClient(Config.MONGO_URI)
        db = client['test']
        
        feedback_data = {
            "session_id": request.session_id,
            "rating": request.rating,
            "comment": request.comment,
            "timestamp": datetime.now()
        }
        
        db['feedback'].insert_one(feedback_data)
        
        return {"message": "Feedback submitted successfully"}
        
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail="Error submitting feedback")

@app.get("/metrics")
async def get_metrics():
    """Lấy thống kê chatbot"""
    try:
        from pymongo import MongoClient
        client = MongoClient(Config.MONGO_URI)
        db = client['test']
        
        # Thống kê cơ bản
        total_chats = db['chats'].count_documents({})
        total_feedback = db['feedback'].count_documents({})
        
        # Tính rating trung bình
        avg_rating = db['feedback'].aggregate([
            {"$group": {"_id": None, "avg_rating": {"$avg": "$rating"}}}
        ]).next().get('avg_rating', 0)
        
        return {
            "total_chats": total_chats,
            "total_feedback": total_feedback,
            "average_rating": round(avg_rating, 2) if avg_rating else 0
        }
        
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail="Error getting metrics")

@app.post("/retrain")
async def retrain_model(request: RetrainRequest):
    """Retrain model"""
    try:
        # Import train function
        from train import train_model
        
        # Chạy training
        result = train_model(force=request.force)
        
        return {"message": "Model retraining completed", "result": result}
        
    except Exception as e:
        logger.error(f"Error retraining model: {e}")
        raise HTTPException(status_code=500, detail="Error retraining model")

@app.post("/webhook/facebook")
async def facebook_webhook(request: Request):
    """Webhook cho Facebook Messenger"""
    try:
        body = await request.json()
        
        # Verify webhook
        if body.get('object') == 'page':
            for entry in body.get('entry', []):
                for messaging_event in entry.get('messaging', []):
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event.get('message', {}).get('text', '')
                    
                    if message_text:
                        # Xử lý tin nhắn
                        response_text = get_response(
                            user_input=message_text,
                            platform='facebook',
                            user_id=sender_id
                        )
                        
                        # Gửi phản hồi về Facebook
                        messenger_integration.send_message('facebook', sender_id, response_text)
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Facebook webhook error: {e}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")

def generate_quick_replies(intent: int, message: str) -> List[str]:
    """Tạo quick replies dựa trên intent"""
    if intent == 0:  # suggest_cake
        return ["Bánh socola", "Bánh vani", "Bánh trà xanh", "Xem tất cả"]
    elif intent == 1:  # ask_price
        return ["Xem giá", "Đặt hàng", "Liên hệ nhân viên"]
    elif intent == 2:  # connect_staff
        return ["Đồng ý", "Hủy"]
    elif intent == 3:  # ask_promotion
        return ["Xem khuyến mãi", "Đặt hàng ngay"]
    elif intent == 4:  # check_order
        return ["Nhập mã đơn hàng", "Liên hệ hỗ trợ"]
    elif intent == 5:  # custom_cake
        return ["Gửi yêu cầu", "Xem mẫu", "Liên hệ thiết kế"]
    else:
        return ["Trợ giúp", "Liên hệ nhân viên"]

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    ) 