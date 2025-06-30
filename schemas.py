from pydantic import BaseModel
from typing import Optional, List, Dict, Any

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