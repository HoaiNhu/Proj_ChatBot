import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime

# Import local modules
from config.config_chatbot import ChatbotConfig
from utils.logger import logger
from services.learning_system import LearningSystem
from services.messenger_integration import MessengerIntegration
from services.nlp_service import NLPService
from services.response_service import ResponseService

# Đường dẫn model đã train
MODEL_PATH = os.getenv("MODEL_PATH", "./models")

# Khởi tạo các service
nlp_service = NLPService(model_path=MODEL_PATH)
response_service = ResponseService()

# Khởi tạo database cho LearningSystem
from pymongo import MongoClient
client = MongoClient(ChatbotConfig.CHATBOT_MONGO_URI)
db = client[ChatbotConfig.CHATBOT_DB_NAME]
learning_system = LearningSystem(db)

messenger_integration = MessengerIntegration()

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

@app.get("/")
async def root():
    return {
        "message": "Chatbot Support API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    try:
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
    try:
        session_id = request.session_id or str(uuid.uuid4())
        intent, confidence = nlp_service.predict_intent(request.message)
        response_text = response_service.get_response(intent, request.message)
        # Lưu hội thoại để học hỏi
        learning_system.collect_conversation_data(
            user_input=request.message,
            bot_response=response_text,
            intent=intent,
            confidence=confidence
        )
        return ChatResponse(
            text=response_text,
            session_id=session_id,
            intent=intent,
            confidence=confidence
        )
    except Exception as e:
        logger.error(f"Error processing chat: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/webhook/facebook")
async def facebook_webhook(request: Request):
    try:
        body = await request.json()
        if body.get('object') == 'page':
            for entry in body.get('entry', []):
                for messaging_event in entry.get('messaging', []):
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event.get('message', {}).get('text', '')
                    if message_text:
                        intent, confidence = nlp_service.predict_intent(message_text)
                        response_text = response_service.get_response(intent, message_text)
                        learning_system.collect_conversation_data(
                            user_input=message_text,
                            bot_response=response_text,
                            intent=intent,
                            confidence=confidence
                        )
                        messenger_integration.send_message('facebook', sender_id, response_text)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Facebook webhook error: {e}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")

@app.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    try:
        if not 1 <= request.rating <= 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
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
    try:
        total_chats = db['chats'].count_documents({})
        total_feedback = db['feedback'].count_documents({})
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
    try:
        from train import train_model
        result = train_model(force=request.force)
        return {"message": "Model retraining completed", "result": result}
    except Exception as e:
        logger.error(f"Error retraining model: {e}")
        raise HTTPException(status_code=500, detail="Error retraining model")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )