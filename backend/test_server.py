#!/usr/bin/env python3
"""
سرور تست ساده برای عیب‌یابی
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
import uvicorn
from datetime import datetime

app = FastAPI(title="natiq-test", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# وضعیت سرور
server_status = {
    "started": datetime.now().isoformat(),
    "requests": 0
}

@app.get("/")
async def root():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="utf-8">
        <title>natiq-test</title>
        <style>
            body {
                font-family: sans-serif;
                padding: 20px;
                text-align: center;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }
            .container {
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
            }
            h1 { margin-bottom: 20px; }
            .status { color: #4ade80; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✅ natiq-test سرور فعال است</h1>
            <p>این یک سرور تست ساده برای بررسی اتصال است.</p>
            <p class="status">وضعیت: <strong>فعال</strong></p>
            <p>آدرس‌های قابل دسترسی:</p>
            <ul style="text-align: right; list-style: none;">
                <li><a href="/api/health" style="color: white;">/api/health</a> - وضعیت سرور</li>
                <li><a href="/api/test" style="color: white;">/api/test</a> - تست API</li>
            </ul>
        </div>
    </body>
    </html>
    """)

@app.get("/api/health")
async def health_check():
    server_status["requests"] += 1
    return {
        "status": "healthy",
        "service": "natiq-test",
        "version": "1.0",
        "requests": server_status["requests"],
        "uptime": datetime.now().isoformat(),
        "message": "سرور تست به درستی کار می‌کند"
    }

@app.get("/api/test")
async def test_endpoint():
    server_status["requests"] += 1
    return {
        "message": "این یک پاسخ تست از سرور است!",
        "timestamp": datetime.now().isoformat(),
        "request_count": server_status["requests"]
    }

@app.post("/api/chat/{session_id}")
async def chat_test(session_id: str, request: dict):
    server_status["requests"] += 1
    question = request.get("message", "")
    
    return {
        "session_id": session_id,
        "question": question,
        "answer": f"این یک پاسخ تست به سوال '{question}' است.",
        "analysis": {"type": "test", "topic": "تست"},
        "timestamp": datetime.now().isoformat(),
        "server": "natiq-test"
    }

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 سرور تست natiq-test در حال راه‌اندازی...")
    print("🌐 آدرس: http://localhost:8000")
    print("📡 وضعیت: http://localhost:8000/api/health")
    print("💬 تست چت: POST به http://localhost:8000/api/chat/test")
    print("="*50)
    print("برای توقف: Ctrl+C")
    print("="*50 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
