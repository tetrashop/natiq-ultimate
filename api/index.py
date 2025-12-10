"""
ناطق API - فایل اصلی برای Vercel
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import json
from datetime import datetime
import uuid

app = FastAPI(
    title="Natiq API",
    version="5.0.0",
    description="سیستم هوش مصنوعی فارسی"
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory storage
sessions = {}

@app.get("/")
async def root():
    return {"message": "Natiq API", "version": "5.0.0"}

@app.get("/api")
async def api_root():
    return {
        "service": "natiq-api",
        "version": "5.0.0",
        "endpoints": {
            "health": "/api/health",
            "chat": "/api/chat",
            "chat_memory": "/api/chat-memory",
            "status": "/api/status"
        }
    }

@app.get("/api/health")
async def health():
    return JSONResponse({
        "status": "healthy",
        "version": "5.0.0",
        "timestamp": datetime.now().isoformat(),
        "server": "Vercel Serverless",
        "python": "3.9"
    })

@app.post("/api/chat")
async def chat(request: Request):
    """Simple chat endpoint"""
    try:
        data = await request.json()
        user_message = data.get("message", "سلام")
        
        responses = [
            f"سلام! پیام شما: '{user_message}'",
            "سیستم ناطق در حال کار است.",
            "پیام شما دریافت شد.",
            "با موفقیت پردازش شد."
        ]
        
        import random
        response = random.choice(responses)
        
        return JSONResponse({
            "success": True,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": "خطای پردازش",
            "timestamp": datetime.now().isoformat()
        }, status_code=400)

@app.post("/api/chat-memory")
async def chat_memory(request: Request):
    """Chat with memory"""
    try:
        data = await request.json()
        message = data.get("message", "")
        session_id = data.get("session_id", str(uuid.uuid4())[:8])
        
        if session_id not in sessions:
            sessions[session_id] = []
        
        sessions[session_id].append({
            "role": "user",
            "content": message,
            "time": datetime.now().isoformat()
        })
        
        response_text = f"شناسه جلسه: {session_id} | پیام‌های ذخیره شده: {len(sessions[session_id])}"
        
        sessions[session_id].append({
            "role": "assistant",
            "content": response_text,
            "time": datetime.now().isoformat()
        })
        
        return JSONResponse({
            "success": True,
            "response": response_text,
            "session_id": session_id,
            "has_memory": True,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": "خطای حافظه",
            "timestamp": datetime.now().isoformat()
        }, status_code=400)

@app.get("/api/status")
async def status():
    import sys
    return {
        "python_version": sys.version.split()[0],
        "api_version": "5.0.0",
        "active_sessions": len(sessions),
        "timestamp": datetime.now().isoformat()
    }

# Handler for Vercel
handler = Mangum(app)
