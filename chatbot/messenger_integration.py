import requests
import json
from flask import request, jsonify
from logger import logger
from config import Config

class MessengerIntegration:
    def __init__(self):
        self.facebook_token = Config.FACEBOOK_PAGE_ACCESS_TOKEN
        self.facebook_verify_token = Config.FACEBOOK_VERIFY_TOKEN
        self.zalo_token = Config.ZALO_ACCESS_TOKEN
        self.zalo_verify_token = Config.ZALO_VERIFY_TOKEN
    
    def handle_facebook_webhook(self):
        try:
            if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
                if request.args.get('hub.verify_token') == self.facebook_verify_token:
                    logger.info("Facebook webhook verified successfully")
                    return request.args.get('hub.challenge')
                else:
                    logger.error("Facebook webhook verification failed")
                    return 'Forbidden', 403
            
            data = request.json
            if data.get('object') == 'page':
                for entry in data.get('entry', []):
                    for messaging_event in entry.get('messaging', []):
                        if messaging_event.get('message'):
                            user_id = messaging_event['sender']['id']
                            message_text = messaging_event['message'].get('text', '')
                            session_id = messaging_event.get('sessionId')
                            if message_text:
                                logger.info(f"Facebook message from {user_id}: {message_text}")
                                return {
                                    'platform': 'facebook',
                                    'user_id': user_id,
                                    'message': message_text,
                                    'sessionId': session_id
                                }
            return None
        except Exception as e:
            logger.error(f"Lỗi xử lý Facebook webhook: {e}")
            return None
    
    def handle_zalo_webhook(self):
        try:
            data = request.json
            if 'verify_token' in data:
                if data['verify_token'] == self.zalo_verify_token:
                    logger.info("Zalo webhook verified successfully")
                    return jsonify({'status': 'success'})
                else:
                    logger.error("Zalo webhook verification failed")
                    return jsonify({'error': 'Invalid verify token'}), 403
            
            if 'message' in data:
                user_id = data['sender']['id']
                message_text = data['message'].get('text', '')
                session_id = data.get('sessionId')
                if message_text:
                    logger.info(f"Zalo message from {user_id}: {message_text}")
                    return {
                        'platform': 'zalo',
                        'user_id': user_id,
                        'message': message_text,
                        'sessionId': session_id
                    }
            return None
        except Exception as e:
            logger.error(f"Lỗi xử lý Zalo webhook: {e}")
            return None
    
    def send_facebook_message(self, user_id, message):
        try:
            url = f"https://graph.facebook.com/v18.0/me/messages?access_token={self.facebook_token}"
            payload = {
                'recipient': {'id': user_id},
                'message': {
                    'text': message,
                    'quick_replies': [
                        {'content_type': 'text', 'title': 'Gợi ý bánh', 'payload': 'suggest_cake'},
                        {'content_type': 'text', 'title': 'Hỏi giá', 'payload': 'ask_price'},
                        {'content_type': 'text', 'title': 'Liên hệ nhân viên', 'payload': 'connect_staff'}
                    ]
                }
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
    
    def send_zalo_message(self, user_id, message):
        try:
            url = "https://openapi.zalo.me/v2.0/oa/message"
            headers = {
                'access_token': self.zalo_token,
                'Content-Type': 'application/json'
            }
            payload = {
                'recipient': {'user_id': user_id},
                'message': {
                    'text': message,
                    'attachment': {
                        'type': 'template',
                        'payload': {
                            'template_type': 'list',
                            'elements': [
                                {'title': 'Gợi ý bánh', 'subtitle': 'Xem các loại bánh ngon', 'type': 'text', 'payload': 'suggest_cake'},
                                {'title': 'Hỏi giá', 'subtitle': 'Kiểm tra giá bánh', 'type': 'text', 'payload': 'ask_price'},
                                {'title': 'Liên hệ nhân viên', 'subtitle': 'Nói chuyện với nhân viên', 'type': 'text', 'payload': 'connect_staff'}
                            ]
                        }
                    }
                }
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                logger.info(f"Đã gửi tin nhắn Zalo cho {user_id}")
                return True
            else:
                logger.error(f"Lỗi gửi tin nhắn Zalo: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Lỗi gửi tin nhắn Zalo: {e}")
            return False
    
    def send_message(self, platform, user_id, message):
        if platform == 'facebook':
            return self.send_facebook_message(user_id, message)
        elif platform == 'zalo':
            return self.send_zalo_message(user_id, message)
        else:
            logger.error(f"Platform không được hỗ trợ: {platform}")
            return False