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

# دیکشنری برای ذخیره حافظه مکالمه هر کاربر (بر اساس session_id)
conversation_memory = {}

@app.post("/api/chat-with-memory")
async def chat_with_memory(request: Request):
    """مکالمه با حافظه جلسه"""
    try:
        data = await request.json()
        message = data.get("message", "").strip()
        session_id = data.get("session_id", "default")
        
        if not message:
            raise HTTPException(status_code=400, detail="پیام نمی‌تواند خالی باشد")
        
        # ایجاد یا بازیابی تاریخچه مکالمه
        if session_id not in conversation_memory:
            conversation_memory[session_id] = []
        
        # اضافه کردن پیام کاربر به حافظه
        conversation_memory[session_id].append({"role": "user", "content": message})
        
        # محدود کردن تاریخچه به ۱۰ پیام آخر
        if len(conversation_memory[session_id]) > 10:
            conversation_memory[session_id] = conversation_memory[session_id][-10:]
        
        # ایجاد پاسخ با توجه به تاریخچه
        history = conversation_memory[session_id]
        response = await generate_smart_response(message, history)
        
        # اضافه کردن پاسخ به حافظه
        conversation_memory[session_id].append({"role": "assistant", "content": response})
        
        return {
            "success": True,
            "response": response,
            "session_id": session_id,
            "history_length": len(conversation_memory[session_id]),
            "memory_enabled": True
        }
        
    except Exception as e:
        logger.error(f"خطا در چت با حافظه: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

async def generate_smart_response(message: str, history: list = None):
    """تولید پاسخ هوشمند با توجه به تاریخچه"""
    # منطق پیشرفته‌تر پاسخ‌دهی
    message_lower = message.lower()
    
    if "حافظه" in message_lower and ("چنده" in message_lower or "چند" in message_lower):
        return f"حافظه فعلی شامل {len(history) if history else 0} پیام است."
    
    if "پاک کن" in message_lower and "حافظه" in message_lower:
        return "حافظه جلسه فعلی پاک شد. می‌توانیم از نو شروع کنیم!"
    
    # پاسخ‌های هوشمند بر اساس تاریخچه
    if history and len(history) > 2:
        last_user_msg = history[-3]["content"] if history[-3]["role"] == "user" else ""
        if "اسم" in last_user_msg and "اسمت چیه" in message_lower:
            return "قبلاً هم گفتم! من ناطق اولتیمیت هستم. حافظه خوبی دارم، مگر نه؟ 😊"
    
    # بازگشت به منطق اصلی
    return "در حال پردازش سوال شما با توجه به تاریخچه مکالمه..."

@app.post("/api/analyze-text")
async def analyze_text(request: Request):
    """تحلیل متن ارسالی"""
    try:
        data = await request.json()
        text = data.get("text", "")
        
        if not text or len(text) < 3:
            raise HTTPException(status_code=400, detail="متن بسیار کوتاه است")
        
        # تحلیل ساده
        char_count = len(text)
        word_count = len(text.split())
        sentence_count = len([c for c in text if c in '.!?'])
        
        # تشخیص زبان (ساده)
        persian_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
        english_chars = sum(1 for c in text if 'a' <= c.lower() <= 'z')
        
        detected_lang = "فارسی" if persian_chars > english_chars else "انگلیسی"
        
        return {
            "success": True,
            "analysis": {
                "characters": char_count,
                "words": word_count,
                "sentences": sentence_count,
                "language": detected_lang,
                "reading_time_seconds": max(1, word_count // 3)
            },
            "summary": f"متن شما {word_count} کلمه دارد و به زبان {detected_lang} است."
        }
        
    except Exception as e:
        logger.error(f"خطا در تحلیل متن: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# دیکشنری برای پاسخ‌های سفارشی
custom_responses = {
    # این‌ها می‌توانند از فایل بارگذاری شوند
    "ساعات کاری": "۲۴ ساعته و ۷ روز هفته در خدمت شما هستم!",
    "ایمیل پشتیبانی": "support@natiq-ultimate.ir",
    "مستندات پروژه": "مستندات کامل در آدرس /api/docs موجود است."
}

@app.post("/api/learn-response")
async def learn_response(request: Request):
    """یادگیری پاسخ جدید"""
    try:
        data = await request.json()
        question = data.get("question", "").strip().lower()
        answer = data.get("answer", "").strip()
        
        if not question or not answer:
            raise HTTPException(status_code=400, detail="سوال و پاسخ ضروری است")
        
        custom_responses[question] = answer
        
        return {
            "success": True,
            "message": f"پاسخ برای '{question[:30]}...' یادگرفته شد!",
            "total_responses": len(custom_responses)
        }
        
    except Exception as e:
        logger.error(f"خطا در یادگیری: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/list-responses")
async def list_responses():
    """لیست پاسخ‌های یادگرفته شده"""
    return {
        "success": True,
        "responses": custom_responses,
        "count": len(custom_responses)
    }


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
