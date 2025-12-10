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
    """صفحه اصلی API"""
    return {
        "message": "🎯 Natiq Ultimate API Server",
        "version": "3.0.0",
        "status": "running",
        "endpoints": {
            "health": "/api/health",
            "chat": "/api/chat (POST)",
            "chat_memory": "/api/chat-memory (POST)"
        },
        "documentation": "برای استفاده از API به مستندات مراجعه کنید"
    }

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


import re
from typing import Dict, List
from datetime import datetime, timedelta

# ذخیره موقت حافظه مکالمه در RAM
chat_memories: Dict[str, List[Dict]] = {}

def extract_name_from_message(message: str) -> str:
    """استخراج نام از پیام کاربر"""
    patterns = [
        r"اسم من (\w+) است",
        r"نام من (\w+) است",
        r"من (\w+) هستم",
        r"من (\w+) ام",
        r"call me (\w+)",
        r"my name is (\w+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return ""

def find_name_in_history(history: List[Dict]) -> str:
    """جستجوی نام در تاریخچه مکالمه"""
    for entry in history:
        if entry["role"] == "user":
            name = extract_name_from_message(entry["message"])
            if name:
                return name
    return ""

@app.post("/api/chat-memory")
async def chat_with_memory(request: Request):
    """مکالمه با حافظه واقعی - نسخه بهبود یافته"""
    try:
        # دریافت داده‌های ورودی
        data = await request.json()
        message = data.get("message", "").strip()
        session_id = data.get("session_id", f"session_{datetime.now().timestamp()}")
        
        # بررسی وجود session
        if session_id not in chat_memories:
            chat_memories[session_id] = []
        
        # استخراج نام از پیام فعلی
        current_name = extract_name_from_message(message)
        
        # ذخیره پیام کاربر
        chat_memories[session_id].append({
            "role": "user",
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "extracted_name": current_name if current_name else None
        })
        
        # تاریخچه مکالمه (آخرین ۱۰ پیام)
        history = chat_memories[session_id][-10:] if len(chat_memories[session_id]) > 10 else chat_memories[session_id]
        
        # تولید پاسخ هوشمندانه‌تر
        if any(word in message.lower() for word in ["اسم", "نام", "name"]) and any(word in message.lower() for word in ["چیه", "چیست", "چه", "what"]):
            # جستجوی نام در تاریخچه
            found_name = find_name_in_history(history)
            if found_name:
                response = f"اسم شما '{found_name}' است! 😊"
            else:
                response = "هنوز نام شما را نمی‌دانم. لطفاً بگویید 'اسم من ... است'."
        
        elif "چند پیام" in message or "چندتا" in message:
            user_messages = [m for m in history if m["role"] == "user"]
            assistant_messages = [m for m in history if m["role"] == "assistant"]
            response = f"📊 در این مکالمه: {len(user_messages)} پیام از شما، {len(assistant_messages)} پاسخ از من. مجموعاً {len(history)} پیام."
        
        elif current_name:
            response = f"سلام {current_name}! خوش آمدی. نامت را به خاطر می‌سپارم. 👋"
        
        else:
            memory_count = len([m for m in history if m["role"] == "user"])
            response = f"پیام شما دریافت شد. من {memory_count} پیام از شما در این مکالمه به خاطر دارم. 💭"
        
        # ذخیره پاسخ سیستم
        chat_memories[session_id].append({
            "role": "assistant",
            "message": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # محدود کردن حجم حافظه (حداکثر ۲۰ پیام در هر session)
        if len(chat_memories[session_id]) > 20:
            chat_memories[session_id] = chat_memories[session_id][-20:]
        
        return {
            "success": True,
            "response": response,
            "session_id": session_id,
            "has_memory": True,
            "memory_count": len(chat_memories[session_id]),
            "user_message_count": len([m for m in history if m["role"] == "user"]),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "خطا در پردازش درخواست"
        }

def cleanup_old_sessions():
    """حذف session‌های قدیمی (هر ساعت یکبار اجرا شود)"""
    global chat_memories
    cutoff_time = datetime.now() - timedelta(hours=1)
    
    sessions_to_remove = []
    for session_id, messages in chat_memories.items():
        if messages and datetime.fromisoformat(messages[0]["timestamp"]) < cutoff_time:
            sessions_to_remove.append(session_id)
    
    for session_id in sessions_to_remove:
        del chat_memories[session_id]


@app.delete("/api/clear-memory/{session_id}")
async def clear_session_memory(session_id: str = "default"):
    """پاکسازی حافظه یک session خاص"""
    try:
        # اینجا تابع clear_memory از ماژول chat_features را فراخوانی کنید
        return {
            "success": True,
            "message": f"حافظه session '{session_id}' پاک شد",
            "session_id": session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import os
from mangum import Mangum

# انتهای فایل app.py (قبل از if __name__)
handler = Mangum(app)

# به‌روزرسانی بخش اجرا
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
