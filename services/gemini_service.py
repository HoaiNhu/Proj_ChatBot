"""
Gemini Service - Sử dụng Google Gemini API để cải thiện response
Làm cho câu trả lời tự nhiên và mượt mà hơn
"""
import os
from typing import Optional
import google.generativeai as genai
from config.config_chatbot import ChatbotConfig

class GeminiService:
    def __init__(self):
        """Khởi tạo Gemini API"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("⚠️ GEMINI_API_KEY không được cấu hình trong .env")
            self.enabled = False
            return
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.enabled = True
        print("✅ Gemini API đã được khởi tạo")
    
    def enhance_response(self, base_response: str, user_message: str, intent: str, context: dict = None) -> str:
        """
        Cải thiện response bằng Gemini API
        
        Args:
            base_response: Response gốc từ chatbot
            user_message: Tin nhắn của user
            intent: Intent đã detect
            context: Context conversation (optional)
        
        Returns:
            Enhanced response tự nhiên hơn, bỏ những dấu **, mỗi thông tin sẽ nằm trên một dòng.
        """
        if not self.enabled:
            return base_response
        
        try:
            # Tạo prompt cho Gemini
            prompt = self._create_enhancement_prompt(base_response, user_message, intent, context)
            
            # Gọi Gemini API
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                enhanced = response.text.strip()
                # Giới hạn độ dài response
                if len(enhanced) > 500:
                    enhanced = enhanced[:497] + "..."
                return enhanced
            else:
                return base_response
                
        except Exception as e:
            print(f"❌ Lỗi khi gọi Gemini API: {e}")
            return base_response
    
    def _create_enhancement_prompt(self, base_response: str, user_message: str, intent: str, context: dict = None) -> str:
        """Tạo prompt để enhance response"""
        
        # Thêm context nếu có
        context_info = ""
        if context:
            last_messages = context.get('last_messages', [])
            if last_messages:
                context_info = "\n\nLịch sử hội thoại gần đây:\n"
                for msg in last_messages[-3:]:  # Lấy 3 tin nhắn gần nhất
                    sender = msg.get('sender', 'user')
                    text = msg.get('text', '')
                    context_info += f"- {sender}: {text}\n"
        
        prompt = f"""Bạn là chatbot hỗ trợ khách hàng của một cửa hàng bánh ngọt. Nhiệm vụ của bạn là làm cho câu trả lời tự nhiên, thân thiện và mượt mà hơn.

Câu hỏi của khách: {user_message}
Intent phát hiện: {intent}
{context_info}

Câu trả lời gốc của hệ thống: {base_response}

Hãy viết lại câu trả lời sao cho:
1. Tự nhiên và thân thiện hơn (giữ giọng điệu phù hợp với cửa hàng bánh)
2. Ngắn gọn, súc tích (không quá 3-4 câu)
3. Giữ nguyên tất cả thông tin quan trọng (giá, tên bánh, địa chỉ, số điện thoại...)
4. Không thêm thông tin không có trong câu trả lời gốc
5. Sử dụng emoji phù hợp (1-2 emoji) để thân thiện hơn
6. Kết thúc bằng câu hỏi mở hoặc lời mời nếu phù hợp

Chỉ trả lời câu đã được cải thiện, không giải thích thêm:"""
        
        return prompt
    
    def generate_conversational_response(self, user_message: str, intent: str, available_data: dict = None) -> str:
        """
        Tạo response hoàn toàn mới từ Gemini dựa trên intent và data
        Dùng cho các trường hợp phức tạp hoặc khi không có template sẵn
        
        Args:
            user_message: Tin nhắn của user
            intent: Intent đã detect
            available_data: Data có sẵn từ database (sản phẩm, giá, khuyến mãi...)
        
        Returns:
            Response được tạo bởi Gemini
        """
        if not self.enabled:
            return "Xin lỗi, tôi không thể trả lời câu hỏi này lúc này."
        
        try:
            data_info = ""
            if available_data:
                data_info = f"\n\nThông tin có sẵn: {str(available_data)[:500]}"  # Giới hạn 500 ký tự
            
            prompt = f"""Bạn là chatbot hỗ trợ của cửa hàng bánh ngọt. Khách hàng đang hỏi:

"{user_message}"

Intent: {intent}
{data_info}

Hãy trả lời khách hàng một cách:
- Thân thiện, tự nhiên
- Ngắn gọn (2-3 câu)
- Chính xác với thông tin có sẵn
- Không bịa đặt thông tin
- Có emoji phù hợp

Chỉ trả lời câu văn, không giải thích:"""
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                return response.text.strip()
            else:
                return "Xin lỗi, tôi không thể trả lời câu hỏi này lúc này."
                
        except Exception as e:
            print(f"❌ Lỗi khi generate response với Gemini: {e}")
            return "Xin lỗi, tôi không thể trả lời câu hỏi này lúc này."

# Singleton instance
_gemini_service = None

def get_gemini_service() -> GeminiService:
    """Lấy Gemini service instance (singleton)"""
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service
