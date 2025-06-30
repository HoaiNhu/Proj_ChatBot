import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime
import random

# Import local modules
from config.config_chatbot import ChatbotConfig
from utils.logger import logger
from services.learning_system import LearningSystem
from services.messenger_integration import MessengerIntegration
from services.nlp_service import NLPService
from services.response_service import ResponseService
from services.conversation_service import ConversationService
from logic.intent_list import INTENT_LIST
from logic.context_rules import CONTEXT_RULES
from logic.intent_rules import INTENT_RESPONSES
from schemas import ChatRequest, ChatResponse, FeedbackRequest, ProductRequest, RetrainRequest

# Đường dẫn model đã train
MODEL_PATH = os.getenv("MODEL_PATH", "./models")

# Khởi tạo các service
nlp_service = NLPService(model_path=MODEL_PATH)
response_service = ResponseService()
conversation_service = ConversationService(model_path=MODEL_PATH)

# Khởi tạo database cho LearningSystem
from pymongo import MongoClient
# Kết nối MongoDB cửa hàng (nếu cần dùng cho training)
store_client = MongoClient(ChatbotConfig.STORE_MONGO_URI)
store_db = store_client[ChatbotConfig.STORE_DB_NAME]

# Kết nối MongoDB chatbot (lưu hội thoại)
chatbot_client = MongoClient(ChatbotConfig.CHATBOT_MONGO_URI)
chatbot_db = chatbot_client[ChatbotConfig.CHATBOT_DB_NAME]
learning_system = LearningSystem(chatbot_db)
db = chatbot_db  # Đảm bảo các API khác cũng dùng đúng db chatbot

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

# Thay thế các model Pydantic bằng import từ schemas.py

def intent_index_to_name(idx):
    if isinstance(idx, int) and 0 <= idx < len(INTENT_LIST):
        return INTENT_LIST[idx]
    return str(idx)

def get_context_action(current_intent, last_bot_intent):
    for rule in CONTEXT_RULES:
        rule_intent, rule_last_bot_intent, rule_action = rule
        if current_intent == rule_intent and (rule_last_bot_intent is None or last_bot_intent == rule_last_bot_intent):
            return rule_action
    return None

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
        chatbot_client.admin.command('ping')
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
        
        # Kiểm tra nếu là session mới, xóa context cũ
        if not request.session_id:
            conversation_service.clear_context()
        
        # Lấy context (lịch sử hội thoại) từ MongoDB
        session = chatbot_db["conversations"].find_one({"sessionId": session_id})
        context = session["messages"] if session and "messages" in session else []
        
        # Lấy intent gần nhất của bot (nếu có)
        last_bot_intent = None
        for msg in reversed(context):
            if msg.get("sender") == "bot" and msg.get("intent") is not None:
                last_bot_intent = intent_index_to_name(msg["intent"])
                break
        
        # Cập nhật context entities TRƯỚC khi detect intent để context luôn mới nhất
        conversation_service.extract_entities(request.message)
        
        # Xác định intent, confidence cho message hiện tại
        intent, confidence = conversation_service.detect_intent(request.message)
        
        # Chuyển đổi intent về dạng integer nếu cần
        intent_index = intent
        intent_name = intent
        if isinstance(intent, str):
            try:
                intent_index = INTENT_LIST.index(intent)
            except ValueError:
                intent_index = 0
                intent_name = INTENT_LIST[0] if INTENT_LIST else "greeting"
                logger.warning(f"Intent '{intent}' not found in INTENT_LIST, using fallback: {intent_name}")
        else:
            intent_name = intent_index_to_name(intent)
        
        # --- Handoff staff logic ---
        # Nếu intent là connect_staff thì cập nhật status escalated
        if intent_name == "connect_staff":
            chatbot_db["conversations"].update_one(
                {"sessionId": session_id},
                {"$set": {"status": "escalated", "updatedAt": datetime.now()}},
                upsert=True
            )
        
        # Kiểm tra nếu status là escalated thì chỉ trả lời 1 câu chờ nhân viên
        session = chatbot_db["conversations"].find_one({"sessionId": session_id})
        if session and session.get("status") == "escalated" and intent_name != "connect_staff":
            return ChatResponse(
                text="Bạn vui lòng chờ một chút, nhân viên sẽ hỗ trợ bạn ngay lập tức!",
                session_id=session_id,
                intent=INTENT_LIST.index("connect_staff"),
                confidence=1.0
            )
        # --- End handoff staff logic ---
        
        # Lấy context_action từ conversation service (lúc này context đã mới nhất)
        context_action = conversation_service.get_context_action(intent_name, request.message)
        
        # Debug: In ra context_action
        print(f"DEBUG - Message: {request.message}")
        print(f"DEBUG - Current cake in context: {conversation_service.conversation_context.get('current_cake', 'None')}")
        print(f"DEBUG - Context Action: {context_action}")
        print(f"DEBUG - Intent: {intent_name}")
        
        # Nếu có context_action, truyền vào response_service.get_response
        if context_action:
            response_text = response_service.get_response(intent_index, request.message, context_action=context_action, last_bot_intent=last_bot_intent)
        else:
            response_text = response_service.get_response(intent_index, request.message)
        
        # Debug: In ra response_text
        print(f"DEBUG - Response: {response_text}")
        print("-" * 50)
        
        # Sau khi có response, mới update_context
        conversation_service.update_context(request.message, intent_name, response_text)
        
        # Lưu hội thoại mới vào messages array của session
        chatbot_db["conversations"].update_one(
            {"sessionId": session_id},
            {"$push": {"messages": {
                "text": request.message,
                "sender": "user",
                "timestamp": datetime.now(),
                "intent": intent_index,
                "confidence": confidence
            }}},
            upsert=True
        )
        chatbot_db["conversations"].update_one(
            {"sessionId": session_id},
            {"$push": {"messages": {
                "text": response_text,
                "sender": "bot",
                "timestamp": datetime.now(),
                "intent": intent_index,
                "confidence": confidence
            }}}
        )
        
        # Lưu vào collection conversation để training nếu cần
        learning_system.collect_conversation_data(
            user_input=request.message,
            bot_response=response_text,
            intent=intent_index,
            confidence=confidence
        )
        
        return ChatResponse(
            text=response_text,
            session_id=session_id,
            intent=intent_index,
            confidence=confidence
        )
    except Exception as e:
        logger.error(f"Error processing chat: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/webhook/facebook")
async def facebook_webhook_verification(request: Request):
    """Xác thực webhook Facebook"""
    try:
        query_params = dict(request.query_params)
        mode = query_params.get('hub.mode')
        token = query_params.get('hub.verify_token')
        challenge = query_params.get('hub.challenge')
        
        if mode == 'subscribe' and token == ChatbotConfig.FACEBOOK_VERIFY_TOKEN:
            logger.info("Facebook webhook verified successfully")
            return int(challenge)
        else:
            logger.error("Facebook webhook verification failed")
            raise HTTPException(status_code=403, detail="Forbidden")
    except Exception as e:
        logger.error(f"Facebook webhook verification error: {e}")
        raise HTTPException(status_code=500, detail="Webhook verification failed")

@app.post("/webhook/facebook")
async def facebook_webhook(request: Request):
    """Xử lý tin nhắn từ Facebook Messenger"""
    try:
        body = await request.json()
        if body.get('object') == 'page':
            for entry in body.get('entry', []):
                for messaging_event in entry.get('messaging', []):
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event.get('message', {}).get('text', '')
                    
                    if message_text:
                        logger.info(f"Facebook message from {sender_id}: {message_text}")
                        
                        # Tạo hoặc lấy session cho user này
                        session_id = f"fb_{sender_id}"
                        
                        # Lấy context (lịch sử hội thoại) từ MongoDB
                        session = chatbot_db["conversations"].find_one({"sessionId": session_id})
                        context = session["messages"] if session and "messages" in session else []

                        # Lấy intent gần nhất của bot (nếu có)
                        last_bot_intent = None
                        for msg in reversed(context):
                            if msg.get("sender") == "bot" and msg.get("intent"):
                                last_bot_intent = msg["intent"]
                                break

                        # Xử lý context đơn giản
                        if last_bot_intent == "ask_address" and "tại shop" in message_text.lower():
                            shop_info = store_db['shop_info'].find_one()
                            address = shop_info.get('address', 'Shop chưa cập nhật địa chỉ') if shop_info else "Shop chưa cập nhật địa chỉ"
                            response_text = f"Địa chỉ shop: {address}"
                            intent = "ask_address"
                            confidence = 1.0
                        else:
                            # Xử lý như cũ
                            intent, confidence = nlp_service.predict_intent(message_text)
                            # Chuyển intent index về intent name nếu cần
                            intent_name = intent
                            if isinstance(intent, int) and 0 <= intent < len(INTENT_LIST):
                                intent_name = INTENT_LIST[intent]
                            # Nếu intent là connect_staff thì cập nhật status escalated
                            if intent_name == "connect_staff":
                                chatbot_db["conversations"].update_one(
                                    {"sessionId": session_id},
                                    {"$set": {"status": "escalated", "updatedAt": datetime.now()}},
                                    upsert=True
                                )
                            # Kiểm tra nếu status escalated thì chỉ trả lời 1 câu chờ nhân viên
                            session = chatbot_db["conversations"].find_one({"sessionId": session_id})
                            if session and session.get("status") == "escalated" and intent_name != "connect_staff":
                                response_text = "Bạn vui lòng chờ một chút, nhân viên sẽ hỗ trợ bạn ngay lập tức!"
                                intent = INTENT_LIST.index("connect_staff")
                                confidence = 1.0
                            else:
                                response_text = response_service.get_response(intent, message_text)

                        # Lưu hội thoại mới vào messages array của session
                        chatbot_db["conversations"].update_one(
                            {"sessionId": session_id},
                            {"$push": {"messages": {
                                "text": message_text,
                                "sender": "user",
                                "timestamp": datetime.now(),
                                "intent": None,
                                "confidence": 0
                            }}},
                            upsert=True
                        )
                        chatbot_db["conversations"].update_one(
                            {"sessionId": session_id},
                            {"$push": {"messages": {
                                "text": response_text,
                                "sender": "bot",
                                "timestamp": datetime.now(),
                                "intent": intent,
                                "confidence": confidence
                            }}}
                        )

                        # Lưu vào collection conversation để training nếu cần
                        learning_system.collect_conversation_data(
                            user_input=message_text,
                            bot_response=response_text,
                            intent=intent,
                            confidence=confidence
                        )

                        # Gửi phản hồi qua Facebook Messenger
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

@app.post("/clear-context")
async def clear_context():
    """Xóa context của cuộc hội thoại hiện tại"""
    try:
        conversation_service.clear_context()
        return {"message": "Context cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing context: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )