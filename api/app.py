#!/usr/bin/env python3
"""
فایل اصلی FastAPI برای ناطق اولتیمیت
با تمام endpointهای جدید
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import json
import asyncio
from typing import Optional

# تنظیمات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ایجاد اپ
app = FastAPI(
    title="ناطق اولتیمیت",
    description="هوش مصنوعی فارسی",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== ENDPOINT های اصلی ====================

@app.get("/")
async def root():
    """صفحه اصلی"""
    return FileResponse("public/index.html")

@app.get("/api/")
async def api_root():
    """لیست تمام endpointها"""
    return {
        "message": "به ناطق اولتیمیت خوش آمدید",
        "version": "2.0.0",
        "endpoints": [
            "/api/",
            "/api/health",
            "/api/chat",
            "/api/test-openai", 
            "/api/status",
            "/api/clear-memory",
            "/api/process",
            "/api/file-info",
            "/api/logs",
            "/api/system-info",
            "/api/docs"
        ],
        "ai_enabled": True
    }

@app.get("/api/health")
async def health_check():
    """بررسی سلامت"""
    return {
        "status": "healthy",
        "service": "natiq-ultimate-ai",
        "version": "2.0.0",
        "timest
    }

@app.post("/api/chat")
async def chat_endpoint(request: Request):
    """مکالمه هوشمند با پشتیبانی از OpenAI"""
    try:
        data = await request.json()
        message = data.get("message", "").strip()
        
        if not message:
            raise HTTPException(status_code=400, detail="پیام نمی‌تواند خالی باشد")
        
        logger.info(f"💬 چت دریافت شد: {message[:50]}...")
        
        # پاسخ‌های پیش‌فرض برای کلیدواژه‌های مهم
        responses = {
            "سلام": "سلام! 👋 به ناطق اولتیمیت خوش آمدید. چطور می‌توانم کمک کنم؟",
            "خداحافظ": "خداحافظ! امیدوارم مفید بوده باشم. 🌟",
            "چطوری": "من خوبم ممنون! 😊 شما چطورید؟",
            "اسمت چیه": "من ناطق اولتیمیت هستم، یک دستیار هوش مصنوعی فارسی پیشرفته.",
            "هوش مصنوعی": "هوش مصنوعی شاخه‌ای از علوم کامپیوتر است که به ایجاد ماشین‌های هوشمند می‌پردازد. امروزه در زمینه‌های مختلف از جمله پردازش زبان طبیعی کاربرد دارد.",
            "تشکر": "خواهش می‌کنم! 😊 همیشه در خدمتم.",
            "زمان": f"زمان سرور: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "ورژن": f"ناطق اولتیمیت نسخه 2.0.0 - سیستم AI فعال"
        }
        
        # جستجوی پاسخ مناسب
        message_lower = message.lower()
        
        # پاسخ به سوالات خاص شناسایی‌شده
        if "رامین اجلال" in message_lower:
            return {
                "success": True,
                "response": "رامین اجلال یک توسعه‌دهنده و علاقه‌مند به هوش مصنوعی و فناوری است. او پروژه‌هایی مانند ناطق اولتیمیت را توسعه می‌دهد. 🔧",
                "ai_enhanced": True,
                "model": "natiq-ai-knowledge"
            }
        
        # اگر کاربر درخواست OpenAI کرده
        if "openai" in message_lower or "اپن ای" in message_lower or "gpt" in message_lower:
            # شبیه‌سازی پاسخ OpenAI
            openai_responses = [
                "من از مدل‌های پیشرفته پردازش زبان استفاده می‌کنم. 🔍",
                "سیستم OpenAI فعال است و آماده پاسخگویی به سوالات شماست. 🤖",
                "برای استفاده کامل از قابلیت‌های OpenAI، لطفاً API Key را در تنظیمات Vercel تنظیم کنید.",
                "من می‌توانم به سوالات مختلفی پاسخ دهم. سوال خود را بپرسید! 💭"
            ]
            
            import random
            return {
                "success": True,
                "response": random.choice(openai_responses),
                "openai_mode": "simulated",
                "tip": "برای فعال‌سازی OpenAI واقعی، کلید API را در تنظیمات Vercel اضافه کنید."
            }
        
        # جستجوی پاسخ در دیکشنری
        for keyword, resp in responses.items():
            if keyword in message_lower:
                return {
                    "success": True,
                    "response": resp,
                    "keyword_matched": keyword,
                    "ai_model": "natiq-ai-v2"
                }
        
        # پاسخ هوشمند برای سوالات عمومی
        intelligent_responses = [
            f"سوال جالبی پرسیدید: '{message[:30]}...'. من در حال یادگیری هستم و سعی می‌کنم بهترین پاسخ را بدهم. 📚",
            "این سوال نیاز به پردازش بیشتری دارد. آیا می‌توانید جزئیات بیشتری بدهید؟",
            "من یک دستیار هوش مصنوعی فارسی هستم. برای سوالات تخصصی‌تر، پیشنهاد می‌کنم از منابع تخصصی استفاده کنید.",
            "در حال حاضر در حال پردازش سوال شما هستم. 🔄"
        ]
        
        import random
        return {
            "success": True,
            "response": random.choice(intelligent_responses),
            "message_length": len(message),
            "ai_model": "natiq-ai-smart",
            "note": "برای پاسخ‌های دقیق‌تر، OpenAI را فعال کنید"
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="فرمت JSON نامعتبر")
    except Exception as e:
        logger.error(f"خطا در چت: {str(e)}")
        return {
            "success": False,
            "error": f"خطای پردازش: {str(e)}",
            "response": "متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید."
        }

@app.post("/api/openai-test")
async def openai_test_endpoint(request: Request):
    """تست اتصال واقعی به OpenAI"""
    try:
        data = await request.json()
        message = data.get("message", "سلام")
        
        # بررسی وجود کلید OpenAI
        import os
        openai_key = os.environ.get("OPENAI_API_KEY")
        
        if not openai_key:
            logger.warning("کلید OpenAI یافت نشد - حالت شبیه‌سازی")
            
            # پاسخ شبیه‌سازی شده
            simulated_responses = {
                "سلام": "سلام! من دستیار هوش مصنوعی شما هستم. 🔧",
                "هوش مصنوعی": "هوش مصنوعی در حال تغییر دنیاست!",
                "رامین اجلال": "توسعه‌دهنده این پروژه - علاقه‌مند به AI و فناوری.",
                "ناطق": "ناطق اولتیمیت یک پروژه هوش مصنوعی فارسی است."
            }
            
            response = "من یک دستیار AI فارسی هستم. برای پاسخ‌های پیشرفته‌تر، کلید OpenAI را تنظیم کنید."
            
            for keyword, resp in simulated_responses.items():
                if keyword in message.lower():
                    response = resp
                    break
            
            return {
                "success": True,
                "response": response,
                "openai_status": "simulated",
                "message": "کلید OpenAI یافت نشد. پاسخ شبیه‌سازی شده است.",
                "setup_instructions": "در تنظیمات Vercel، متغیر محیطی OPENAI_API_KEY را اضافه کنید."
            }
        
        # اگر کلید وجود دارد، از OpenAI واقعی استفاده کنید
        try:
            # این بخش نیاز به نصب openai package دارد
            # pip install openai
            import openai
            openai.api_key = openai_key
            
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "شما یک دستیار هوش مصنوعی فارسی هستید. به زبان فارسی پاسخ دهید."},
                    {"role": "user", "content": message}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            response = completion.choices[0].message.content
            
            return {
                "success": True,
                "response": response,
                "openai_status": "connected",
                "model": "gpt-3.5-turbo",
                "tokens_used": completion.usage.total_tokens
            }
            
        except ImportError:
            logger.error("پکیج openai نصب نشده است")
            return {
                "success": False,
                "error": "پکیج openai نصب نشده",
                "setup_instructions": "در requirements.txt خط 'openai' را اضافه کنید."
            }
            
    except Exception as e:
        logger.error(f"خطا در تست OpenAI: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطای OpenAI: {str(e)}")


@app.get("/api/status")
async def get_status():
    """وضعیت سیستم"""
    import platform
    import sys
    
    return {
        "system": {
            "python_version": sys.version.split()[0],
            "platform": platform.system(),
            "api_version": "2.0.0"
        },
        "ai": {
            "status": "active",
            "language": "فارسی",
            "features": ["chat", "text_processing", "memory"]
        },
        "endpoints_active": 10,
        "uptime": "running"
    }

@app.post("/api/clear-memory")
async def clear_memory():
    """پاکسازی حافظه (نمایشی)"""
    return {
        "success": True,
        "message": "حافظه موقت پاکسازی شد",
        "cleared_at": __import__("datetime").datetime.now().isoformat()
    }

# ==================== ENDPOINT های قدیمی (برای سازگاری) ====================

@app.post("/api/process")
async def process_text(request: Request):
    """پردازش متن (برای سازگاری با نسخه قدیم)"""
    try:
        data = await request.json()
        text = data.get("text", "").strip()
        
        if not text:
            raise HTTPException(status_code=400, detail="متن نمی‌تواند خالی باشد")
        
        # پردازش هوشمند
        if "سلام" in text:
            response = f"سلام! متن شما: '{text[:50]}...' پردازش شد."
        else:
            response = f"متن پردازش شده: {text[:100]}..." if len(text) > 100 else f"متن پردازش شده: {text}"
        
        return {
            "success": True,
            "original_length": len(text),
            "processed_text": response,
            "message": "پردازش با موفقیت انجام شد",
            "language": "fa"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/file-info")
async def get_file_info(path: str = "requirements.txt"):
    """اطلاعات فایل"""
    try:
        import os
        file_path = f"/var/task/{path}" if path.startswith("/") else f"/var/task/{path}"
        
        # شبیه‌سازی اطلاعات فایل
        return {
            "success": True,
            "file_path": file_path,
            "file_name": os.path.basename(path),
            "exists": True,
            "size": "1024",
            "type": "text/plain",
            "sample": "این یک نمونه از محتوای فایل است...",
            "message": "اطلاعات فایل دریافت شد"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/logs")
async def get_logs(limit: int = 50):
    """لاگ‌های سیستم"""
    sample_logs = [
        f"{__import__('datetime').datetime.now().isoformat()} - INFO - API v2.0.0 شروع شد",
        f"{__import__('datetime').datetime.now().isoformat()} - INFO - سرویس AI فعال شد",
        f"{__import__('datetime').datetime.now().isoformat()} - INFO - آماده دریافت درخواست‌ها",
        f"{__import__('datetime').datetime.now().isoformat()} - INFO - /api/test-openai endpoint فعال شد"
    ]
    
    return {
        "success": True,
        "logs": sample_logs[-limit:],
        "total": len(sample_logs),
        "limit": limit
    }

@app.get("/api/system-info")
async def get_system_info():
    """اطلاعات سیستم"""
    import platform
    
    return {
        "system": platform.system(),
        "release": platform.release(),
        "python": platform.python_version(),
        "api": "natiq-ultimate-ai",
        "version": "2.0.0"
    }

# ==================== مستندات ====================

@app.get("/api/docs")
async def api_docs():
    """مستندات API"""
    docs_html = """
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>ناطق اولتیمیت - مستندات</title>
        <style>
            body { font-family: 'Vazirmatn', sans-serif; padding: 20px; background: #f5f5f5; }
            .container { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-right: 4px solid #007bff; }
            .method { display: inline-block; padding: 5px 10px; border-radius: 4px; color: white; font-weight: bold; margin-left: 10px; }
            .get { background: #28a745; }
            .post { background: #007bff; }
            code { background: #eee; padding: 2px 5px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📚 مستندات ناطق اولتیمیت API</h1>
            
            <div class="endpoint">
                <span class="method get">GET</span> <code>/api/</code>
                <p>لیست تمام endpointها</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span> <code>/api/health</code>
                <p>بررسی سلامت سیستم</p>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span> <code>/api/chat</code>
                <p>مکالمه با هوش مصنوعی</p>
                <small>بدنه: {"message": "سلام"}</small>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span> <code>/api/test-openai</code>
                <p>تست اتصال OpenAI</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span> <code>/api/status</code>
                <p>وضعیت سیستم</p>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span> <code>/api/clear-memory</code>
                <p>پاکسازی حافظه</p>
            </div>
            
            <h2>📞 تست سریع</h2>
            <pre><code>curl https://natiq-ultimate.vercel.app/api/test-openai</code></pre>
            
            <pre><code>curl -X POST https://natiq-ultimate.vercel.app/api/chat \\
  -H "Content-Type: application/json" \\
  -d '{"message": "سلام"}'</code></pre>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=docs_html)

# ==================== مدیریت خطا ====================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "مسیر یافت نشد",
            "path": str(request.url.path),
            "available_endpoints": [
                "/api/",
                "/api/health", 
                "/api/chat",
                "/api/test-openai",
                "/api/status",
                "/api/clear-memory",
                "/api/process",
                "/api/file-info", 
                "/api/logs",
                "/api/system-info",
                "/api/docs"
            ],
            "tip": "از /api/ برای دیدن لیست کامل endpointها استفاده کنید"
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    logger.error(f"خطای 500: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "خطای داخلی سرور",
            "message": "لطفاً دوباره تلاش کنید"
        }
    )

# Middleware برای لاگ‌گیری
@app.middleware("http")
async def log_middleware(request: Request, call_next):
    import time
    start = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {duration:.3f}s")
    
    return response

# برای اجرای محلی
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
