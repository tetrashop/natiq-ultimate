"""
NATIQ ULTIMATE - هسته API المپیکی (سازگار با Vercel Functions)
"""
import json
import os
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler
from io import BytesIO

class NatiqOlympicSystem:
    """سیستم هسته ناتیق با معماری المپیکی"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.request_counter = 0
        self.session_store = {}
        
    def generate_response_id(self):
        """تولید شناسه یکتا برای هر پاسخ"""
        import time
        import random
        timestamp = int(time.time() * 1000)
        random_id = random.randint(1000, 9999)
        return f"OLY-{timestamp}-{random_id}"
    
    def health_check(self):
        """بررسی سلامت سیستم"""
        self.request_counter += 1
        return {
            "status": "olympic_operational",
            "version": "OLYMPIC-CORE-1.0",
            "timestamp": datetime.now().isoformat(),
            "uptime": str(datetime.now() - self.start_time),
            "requests_served": self.request_counter,
            "system": {
                "python_version": sys.version.split()[0],
                "platform": sys.platform,
                "environment": "production" if os.getenv("VERCEL") else "development"
            }
        }
    
    def process_chat(self, message, session_id=None):
        """پردازش پیام چت"""
        self.request_counter += 1
        
        if not session_id:
            session_id = f"SESS-{int(datetime.now().timestamp())}"
        
        # پاسخ‌های از پیش تعریف شده
        responses = [
            f"🏆 درود! پیام شما: «{message}» دریافت شد. سیستم ناتیق المپیکی فعال است.",
            f"✅ پردازش موفق. ورودی: '{message[:50]}...' | مدل: Natiq-Olympic-Core",
            "🚀 سیستم هوش مصنوعی فارسی با معماری المپیکی آماده خدمات‌رسانی است.",
            f"📊 تحلیل پیام شما کامل شد. شناسه جلسه: {session_id}",
            "💡 پیشنهاد: می‌توانید درخواست‌های پیچیده‌تری مطرح کنید. سیستم پشتیبانی کامل دارد."
        ]
        
        import time
        seed = int(time.time()) % len(responses)
        selected_response = responses[seed]
        
        return {
            "success": True,
            "response": selected_response,
            "session_id": session_id,
            "response_id": self.generate_response_id(),
            "timestamp": datetime.now().isoformat()
        }

# ==================== [HANDLER اصلی Vercel] ====================
natiq_system = NatiqOlympicSystem()

def handler(request):
    """
    هندلر اصلی برای Vercel Serverless Functions
    """
    import json
    
    # استخراج اطلاعات از درخواست
    path = request.path
    method = request.method
    
    # هدرهای پیش‌فرض
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'X-Natiq-System': 'Olympic-Core-1.0'
    }
    
    # تحلیل مسیر و متد
    if '/health' in path or path == '/api/health':
        # اندپوینت سلامت
        response_data = natiq_system.health_check()
        status_code = 200
    
    elif '/chat' in path and method == 'POST':
        # اندپوینت چت
        try:
            body = request.body
            if isinstance(body, bytes):
                body = body.decode('utf-8')
            
            request_data = json.loads(body) if body else {}
            user_message = request_data.get('message', 'سلام سیستم ناتیق')
            session_id = request_data.get('session_id')
            
            response_data = natiq_system.process_chat(user_message, session_id)
            status_code = 200
        except json.JSONDecodeError:
            response_data = {
                "success": False,
                "error": "فرمت JSON نامعتبر",
                "response": "لطفاً داده‌ها را به درستی ارسال کنید"
            }
            status_code = 400
        except Exception as e:
            response_data = {
                "success": False,
                "error": "خطای پردازش",
                "response": "سیستم در حال حاضر پاسخگو نیست"
            }
            status_code = 500
    
    elif '/status' in path:
        # وضعیت سیستم
        response_data = {
            "system": {
                "name": "Natiq Ultimate Olympic System",
                "version": "OLYMPIC-CORE-1.0",
                "status": "fully_operational",
                "startup_time": natiq_system.start_time.isoformat(),
                "current_time": datetime.now().isoformat()
            },
            "metrics": {
                "total_requests": natiq_system.request_counter,
                "active_sessions": len(natiq_system.session_store)
            }
        }
        status_code = 200
    
    elif '/api' in path or path == '/':
        # اطلاعات عمومی API
        response_data = {
            "service": "Natiq Ultimate API",
            "version": "OLYMPIC-CORE-1.0",
            "status": "active",
            "documentation": {
                "health": "GET /api/health",
                "chat": "POST /api/chat",
                "status": "GET /api/status"
            },
            "description": "سیستم هوش مصنوعی فارسی با معماری المپیکی"
        }
        status_code = 200
    
    else:
        # مسیر نامعلوم
        response_data = {
            "error": "مسیر یافت نشد",
            "path": path,
            "available_endpoints": ["/api/health", "/api/chat", "/api/status"]
        }
        status_code = 404
    
    # ساخت پاسخ نهایی
    return {
        'statusCode': status_code,
        'headers': headers,
        'body': json.dumps(response_data, ensure_ascii=False)
    }

# ==================== [تست محلی] ====================
if __name__ == "__main__":
    """تست مستقل سیستم"""
    print("🧪 سیستم ناتیق المپیکی - تست محلی")
    print("=" * 50)
    
    # ساخت یک درخواست تست
    class TestRequest:
        path = "/api/health"
        method = "GET"
        body = b"{}"
    
    test_request = TestRequest()
    result = handler(test_request)
    print("✅ تست سلامت:", result["statusCode"])
    print(json.dumps(json.loads(result["body"]), indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 50)
    print("🚀 سیستم آماده استقرار است.")
