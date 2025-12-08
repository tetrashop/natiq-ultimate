from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import os

# بخش خواندن کلید (این باید وجود داشته باشد)
import os
api_key = os.getenv("OPENAI_API_KEY")  # روش صحیح
# api_key = "sk-..."  # روش غلط (کلید در کد نوشته شده)

app = FastAPI(title="Natiq Ultimate API", version="6.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class QuestionRequest(BaseModel):
    question: str
    user_id: Optional[str] = None

# Storage for conversation history
conversation_history = []

@app.get("/")
async def root():
    return {
        "message": "به API ناطق اولتیمیت خوش آمدید",
        "version": "6.0",
        "status": "active",
        "endpoints": [
            "GET /api/health",
            "POST /api/ask",
            "GET /api/chat/history",
            "GET /api/system/status"
        ]
    }

@app.get("/api/health")
async def health():
    """بررسی سلامت سیستم"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "6.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.post("/api/ask")
async def ask_question(request: QuestionRequest):
    """پردازش سوال کاربر و تولید پاسخ"""
    try:
        user_question = request.question.strip()
        
        if not user_question:
            raise HTTPException(status_code=400, detail="سوال نباید خالی باشد")
        
        # پاسخ هوشمند
        response_text = generate_response(user_question)
        
        # ذخیره در تاریخچه
        conversation_entry = {
            "question": user_question,
            "response": response_text,
            "timestamp": datetime.now().isoformat(),
            "user_id": request.user_id
        }
        conversation_history.append(conversation_entry)
        
        # محدود کردن تاریخچه به ۵۰ مورد
        if len(conversation_history) > 50:
            conversation_history.pop(0)
        
        return {
            "success": True,
            "question": user_question,
            "response": response_text,
            "conversation_id": len(conversation_history),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطا در پردازش: {str(e)}")

@app.get("/api/chat/history")
async def get_chat_history(limit: int = 20):
    """دریافت تاریخچه مکالمات"""
    return {
        "success": True,
        "count": len(conversation_history[-limit:]),
        "history": conversation_history[-limit:],
        "total": len(conversation_history)
    }

@app.get("/api/system/status")
async def system_status():
    """وضعیت کامل سیستم"""
    return {
        "system": "Natiq Ultimate v6.0",
        "status": "operational",
        "api_endpoints": {
            "health": "active",
            "ask": "active", 
            "chat_history": "active",
            "system_status": "active"
        },
        "resources": {
            "memory_usage": "normal",
            "response_time": "optimal",
            "uptime": "100%"
        },
        "timestamp": datetime.now().isoformat()
    }

def generate_response(question: str) -> str:
    """تابع تولید پاسخ هوشمند"""
    question_lower = question.lower()
    
    # پاسخ‌های از پیش تعریف شده
    responses = {
        "سلام": "سلام! چطور می‌توانم کمکتان کنم؟",
        "خداحافظ": "خداحافظ! موفق باشید.",
        "اسمت چیه": "من ناطق اولتیمیت هستم، دستیار هوشمند شما.",
        "حالت چطوره": "عالی هستم! آماده پاسخگویی به سوالات شما.",
        "ممنون": "خواهش می‌کنم! خوشحالم که می‌توانم کمک کنم.",
        "کمک": "بله، من می‌توانم در زمینه‌های مختلف به شما کمک کنم. چه سوالی دارید؟",
        "ورژن": "من نسخه ۶.۰ ناطق اولتیمیت هستم.",
        "ساعت": f"الان ساعت {datetime.now().strftime('%H:%M')} است.",
        "تاریخ": f"امروز {datetime.now().strftime('%Y/%m/%d')} است."
    }
    
    # جستجوی کلیدواژه
    for key, response in responses.items():
        if key in question_lower:
            return response
    
    # پاسخ پیش‌فرض
    return f"شما پرسیدید: '{question}'. من در حال یادگیری هستم و سعی می‌کنم بهترین پاسخ را بدهم!"
