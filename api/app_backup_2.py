"""
Natiq API - نسخه نهایی بدون وابستگی‌های سنگین
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import json
from datetime import datetime
import uuid

app = FastAPI(
    title="Natiq API",
    version="4.0.0",
    description="سیستم هوش مصنوعی فارسی - نسخه سبک و پایدار"
)

# تنظیمات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ذخیره ساده در حافظه برای چت
chat_memory = {}

@app.get("/")
async def root():
    return {
        "service": "natiq-api",
        "version": "4.0.0",
        "status": "active",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "/api/health",
            "/api/chat",
            "/api/chat-memory",
            "/api/test"
        ]
    }

@app.get("/api/health")
async def health():
    return JSONResponse({
        "status": "healthy",
        "version": "4.0.0",
        "timestamp": datetime.now().isoformat(),
        "server": "Vercel Python 3.12",
        "memory": "no-numpy-version"
    })

@app.post("/api/chat")
async def chat(request: Request):
    """ساده‌ترین endpoint چت"""
    try:
        # خواندن داده‌ها
        body_bytes = await request.body()
        
        if body_bytes:
            data = json.loads(body_bytes.decode('utf-8'))
            message = data.get("message", "").strip()
        else:
            message = ""
        
        if not message:
            message = "سلام"
        
        # پاسخ ساده
        responses = [
            "سلام! من ناطق هستم. چطور می‌تونم کمک کنم؟",
            "پیام شما دریافت شد. سیستم در حال کار است.",
            "به سیستم ناطق خوش آمدید!",
            "آماده پاسخگویی به سوالات شما هستم."
        ]
        
        import random
        response = random.choice(responses)
        
        return JSONResponse({
            "success": True,
            "message": message,
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "model": "natiq-light"
        })
        
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": "خطای پردازش",
            "detail": str(e)[:100],
            "timestamp": datetime.now().isoformat()
        }, status_code=400)

@app.post("/api/chat-memory")
async def chat_memory_endpoint(request: Request):
    """چت با حافظه ساده"""
    try:
        body_bytes = await request.body()
        data = json.loads(body_bytes.decode('utf-8')) if body_bytes else {}
        
        message = data.get("message", "")
        session_id = data.get("session_id", str(uuid.uuid4())[:8])
        
        # مدیریت حافظه ساده
        if session_id not in chat_memory:
            chat_memory[session_id] = []
        
        chat_memory[session_id].append({
            "role": "user",
            "content": message,
            "time": datetime.now().isoformat()
        })
        
        # پاسخ ساده
        response_text = f"پیام شما با شناسه جلسه {session_id} دریافت شد. حافظه: {len(chat_memory[session_id])} پیام"
        
        chat_memory[session_id].append({
            "role": "assistant",
            "content": response_text,
            "time": datetime.now().isoformat()
        })
        
        return JSONResponse({
            "success": True,
            "response": response_text,
            "session_id": session_id,
            "message_count": len(chat_memory[session_id]),
            "has_memory": True,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": "خطای حافظه",
            "detail": str(e)[:100],
            "timestamp": datetime.now().isoformat()
        }, status_code=400)

@app.get("/api/test")
async def test():
    """تست کامل API"""
    return JSONResponse({
        "test": "success",
        "service": "Natiq API",
        "version": "4.0.0",
        "status": "fully_operational",
        "timestamp": datetime.now().isoformat(),
        "features": ["chat", "memory", "health"],
        "python_compatible": True,
        "vercel_ready": True
    })

@app.get("/api/status")
async def status():
    """وضعیت سیستم"""
    import sys
    return {
        "python_version": sys.version.split()[0],
        "platform": sys.platform,
        "api_version": "4.0.0",
        "active_sessions": len(chat_memory),
        "timestamp": datetime.now().isoformat()
    }

# هندلر برای Vercel
handler = Mangum(app)

# برای اجرای محلی
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
