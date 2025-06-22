import requests
from flask import request, jsonify
from config.config_chatbot import Config
from utils.logger import logger

class MessengerIntegration:
    def __init__(self):
        self.facebook_token = Config.FACEBOOK_PAGE_ACCESS_TOKEN
        self.facebook_verify_token = Config.FACEBOOK_VERIFY_TOKEN
    
    def handle_facebook_webhook(self):
        """Xử lý webhook từ Facebook Messenger"""
        try:
            # Xác thực webhook
            if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
                if request.args.get('hub.verify_token') == self.facebook_verify_token:
                    logger.info("Facebook webhook verified successfully")
                    return request.args.get('hub.challenge')
                else:
                    logger.error("Facebook webhook verification failed")
                    return 'Forbidden', 403
            
            # Xử lý tin nhắn
            data = request.json
            if data.get('object') == 'page':
                for entry in data.get('entry', []):
                    for messaging_event in entry.get('messaging', []):
                        if messaging_event.get('message'):
                            user_id = messaging_event['sender']['id']
                            message_text = messaging_event['message'].get('text', '')
                            if message_text:
                                logger.info(f"Facebook message from {user_id}: {message_text}")
                                return {
                                    'platform': 'facebook',
                                    'user_id': user_id,
                                    'message': message_text
                                }
            return None
        except Exception as e:
            logger.error(f"Lỗi xử lý Facebook webhook: {e}")
            return None
    
    def send_facebook_message(self, user_id, message):
        """Gửi tin nhắn qua Facebook Messenger"""
        try:
            url = f"https://graph.facebook.com/v18.0/me/messages?access_token={self.facebook_token}"
            payload = {
                'recipient': {'id': user_id},
                'message': {'text': message}
            }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                logger.info(f"Đã gửi tin nhắn Facebook cho {user_id}")
                return True
            else:
                logger.error(f"Lỗi gửi tin nhắn Facebook: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Lỗi gửi tin nhắn Facebook: {e}")
            return False
    
    def send_message(self, platform, user_id, message):
        """Gửi tin nhắn theo platform"""
        if platform == 'facebook':
            return self.send_facebook_message(user_id, message)
        else:
            logger.error(f"Platform không được hỗ trợ: {platform}")
            return False