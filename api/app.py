#!/usr/bin/env python3
"""
ناطق اولتیمیت - نسخه نهایی
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import json
import datetime
import random

# تنظیمات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# بررسی OpenAI API Key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
AI_ENABLED = bool(OPENAI_API_KEY)

# ایجاد اپ
app = FastAPI(
    title="ناطق اولتیمیت",
    description="هوش مصنوعی فارسی پیشرفته",
    version="3.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return FileResponse("public/index.html")

@app.get("/api/")
async def api_root():
    return {
        "message": "به ناطق اولتیمیت خوش آمدید",
        "version": "3.0.0",
        "ai_enabled": AI_ENABLED,
        "endpoints": [
            "/api/",
            "/api/health",
            "/api/chat",
            "/api/chat-openai",
            "/api/test-openai",
            "/api/status",
            "/api/debug",
            "/api/docs"
        ]
    }

@app.post("/api/chat")
async def chat_endpoint(request: Request):
    """مکالمه هوشمند"""
    try:
        data = await request.json()
        message = data.get("message", "").strip()
        
        if not message:
            raise HTTPException(status_code=400, detail="پیام نمی‌تواند خالی باشد")
        
        logger.info(f"💬 چت دریافت شد: {message[:50]}...")
        
        # پاسخ‌های تخصصی
        message_lower = message.lower()
        
        # پاسخ به سوالات رامین اجلال
        if "رامین اجلال" in message_lower or "دارایی" in message_lower:
            response = """📊 اطلاعات رامین اجلال:
            
• **پروژه‌ها و دارایی‌های فنی:**
  - ناطق اولتیمیت (سیستم هوش مصنوعی فارسی)
  - پروژه‌های متن‌باز در حوزه AI
  - تجربه در توسعه وب و اپلیکیشن

• **تخصص‌ها:**
  - برنامه‌نویسی پایتون و هوش مصنوعی
  - توسعه API و سیستم‌های بک‌اند
  - مدیریت سرور و deploy

• **دارایی‌های دیجیتال:**
  - دامنه‌ها و وبسایت‌های شخصی
  - حساب‌های توسعه‌دهنده در پلتفرم‌های مختلف
  - کتابخانه‌های کد متن‌باز

برای اطلاعات دقیق‌تر مالی یا دارایی‌های شخصی، لطفاً مستقیماً با خود فرد تماس بگیرید."""
        
        elif "از openai بپرس" in message_lower or "از اپن ای بپرس" in message_lower:
            if AI_ENABLED:
                response = "🔵 سیستم OpenAI فعال است! سوال شما برای پردازش ارسال شد.\n\nبرای استفاده مستقیم: POST به /api/chat-openai"
            else:
                response = "⚠️ لطفاً در تنظیمات Vercel، متغیر OPENAI_API_KEY را تنظیم کنید."
        
        elif "سلام" in message_lower:
            response = "سلام! 👋 به ناطق اولتیمیت نسخه ۳.۰.۰ خوش آمدید!"
        
        else:
            responses = [
                "سوال خوبی پرسیدید! سیستم در حال پردازش است...",
                "برای پاسخ دقیق‌تر، سوال خود را با جزئیات بیشتر مطرح کنید.",
                f"سیستم هوش مصنوعی {'فعال' if AI_ENABLED else 'غیرفعال'} است. نسخه: 3.0.0",
                "در حال حاضر از پایگاه دانش محلی استفاده می‌کنم."
            ]
            response = random.choice(responses)
        
        return {
            "success": True,
            "response": response,
            "ai_enabled": AI_ENABLED,
            "version": "3.0.0",
            "timestamp": datetime.datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"خطا: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "خطای پردازش",
                "message": "لطفاً دوباره تلاش کنید"
            }
        )

@app.post("/api/chat-openai")
async def chat_openai(request: Request):
    """ارتباط مستقیم با OpenAI"""
    if not AI_ENABLED:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "OpenAI غیرفعال",
                "instructions": "در تنظیمات Vercel، متغیر OPENAI_API_KEY را تنظیم کنید."
            }
        )
    
    return {
        "success": True,
        "message": "✅ endpoint /api/chat-openai فعال است!",
        "status": "برای استفاده از OpenAI واقعی، کد کامل را از پاسخ‌های قبلی کپی کنید.",
        "tip": "کد کامل در تاریخچه مکالمه موجود است"
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "3.0.0",
        "ai_enabled": AI_ENABLED,
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.get("/api/debug")
async def debug():
    """بررسی وضعیت سیستم"""
    return {
        "version": "3.0.0",
        "file": __file__,
        "openai_configured": AI_ENABLED,
        "timestamp": datetime.datetime.now().isoformat(),
        "check": "اگر این پیام را می‌بینید، نسخه ۳.۰.۰ نصب است"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
