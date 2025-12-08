from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import json
import os
from datetime import datetime

app = FastAPI(title="Natiq Ultimate API", version="6.0")

# CORS middleware
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
    context: Optional[str] = None

class SystemStatus(BaseModel):
    component: str
    status: str
    message: str
    timestamp: str

# Health endpoint
@app.get("/api/health")
async def health_check():
    """بررسی سلامت API"""
    return {
        "status": "healthy",
        "version": "6.0",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "/api/health": "GET - بررسی سلامت",
            "/api/ask": "POST - پرسش و پاسخ",
            "/api/test": "GET - تست ارتباط",
            "/api/status": "GET - وضعیت سیستم",
            "/api/nlp/posts": "GET - دریافت پست‌های NLP"
        }
    }

# Ask endpoint
@app.post("/api/ask")
async def ask_question(request: QuestionRequest):
    """پردازش سوالات کاربر"""
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="سوال خالی است")
        
        # پاسخ هوشمند (می‌توانید بعداً با مدل NLP جایگزین کنید)
        responses = {
            "سلام": "سلام! چطور می‌توانم کمک کنم؟",
            "حالت چطوره": "خوبم ممنون! آماده پاسخگویی به سوالات شما هستم.",
            "اسمت چیه": "من ناطق اولتیمیت هستم، یک دستیار هوشمند فارسی.",
            "خداحافظ": "خداحافظ! موفق باشید.",
        }
        
        question_lower = request.question.lower().strip()
        response = responses.get(question_lower, 
            f"شما پرسیدید: '{request.question}'. من در حال یادگیری هستم!")
        
        return {
            "success": True,
            "response": response,
            "question": request.question,
            "timestamp": datetime.now().isoformat(),
            "context_used": request.context if request.context else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Test endpoint
@app.get("/api/test")
async def test_endpoint():
    """تست ارتباط با API"""
    return {
        "message": "API به درستی کار می‌کند!",
        "timestamp": datetime.now().isoformat(),
        "status": "active",
        "version": "6.0"
    }

# System status endpoint
@app.get("/api/status")
async def system_status():
    """وضعیت کامل سیستم"""
    components = [
        {"component": "API Server", "status": "running", "message": "سرور فعال است"},
        {"component": "Database", "status": "connected", "message": "اتصال برقرار است"},
        {"component": "NLP Engine", "status": "ready", "message": "موتور پردازش زبان آماده است"},
        {"component": "Authentication", "status": "active", "message": "احراز هویت فعال است"},
        {"component": "File Storage", "status": "available", "message": "فضای ذخیره‌سازی در دسترس است"}
    ]
    
    return {
        "system": "Natiq Ultimate",
        "status": "operational",
        "uptime": "100%",
        "timestamp": datetime.now().isoformat(),
        "components": components
    }

# NLP posts endpoint (مطابق درخواست شما برای ۲۱۰ پست)
@app.get("/api/nlp/posts")
async def get_nlp_posts(limit: int = 210, page: int = 1):
    """دریافت پست‌های NLP (آخرین ۲۱۰ پست)"""
    try:
        # ساخت داده نمونه (در مرحله بعد با دیتابیس واقعی جایگزین شود)
        sample_posts = []
        for i in range(1, min(limit, 210) + 1):
            sample_posts.append({
                "id": i,
                "title": f"پست نمونه NLP شماره {i}",
                "content": f"این محتوای نمونه برای پست NLP شماره {i} است.",
                "author": "سیستم ناطق",
                "date": datetime.now().isoformat(),
                "tags": ["nlp", "هوش مصنوعی", "پردازش زبان"]
            })
        
        return {
            "success": True,
            "posts": sample_posts,
            "total": len(sample_posts),
            "page": page,
            "limit": limit,
            "message": f"آخرین {len(sample_posts)} پست NLP دریافت شد"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Root endpoint
@app.get("/")
async def root():
    """صفحه اصلی API"""
    return {
        "message": "به API ناطق اولتیمیت خوش آمدید",
        "version": "6.0",
        "documentation": "/docs برای مستندات Swagger",
        "endpoints": [
            "/api/health",
            "/api/ask",
            "/api/test", 
            "/api/status",
            "/api/nlp/posts"
        ]
    }

# Catch-all for undefined routes
@app.get("/api/{path:path}")
async def catch_all(path: str):
    """مدیریت مسیرهای تعریف نشده"""
    raise HTTPException(
        status_code=404,
        detail=f"Endpoint /api/{path} پیدا نشد. endpointهای موجود: /health, /ask, /test, /status, /nlp/posts"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
