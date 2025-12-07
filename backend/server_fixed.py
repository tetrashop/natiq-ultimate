#!/usr/bin/env python3
"""
سرور اصلی natiq-ultimate - نسخه تصحیح شده برای Termux
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
from datetime import datetime
from pathlib import Path
import sys
import os

# اضافه کردن مسیر backend
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# تلاش برای import natiq_smart
try:
    from natiq_smart import NatiqSmart
    NATIQ_READY = True
    print("✅ ماژول natiq_smart بارگذاری شد")
except ImportError:
    print("⚠️  ماژول natiq_smart یافت نشد. استفاده از نسخه ساده...")
    # ایجاد کلاس ساده جایگزین
    class NatiqSmart:
        def __init__(self):
            self.user_name = "کاربر"
            self.stats = {"questions_asked": 0, "topics_covered": set()}
        def analyze_question(self, q): 
            return {"type": "general", "topic": "عمومی"}
        def generate_answer(self, q, a): 
            self.stats["questions_asked"] += 1
            return f"پاسخ به: {q} (در حال راه‌اندازی)"
        def save_conversation(self, q, a): 
            pass
    NATIQ_READY = False

app = FastAPI(title="natiq-ultimate", version="2.1")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# مدیر WebSocket ساده
class ConnectionManager:
    def __init__(self):
        self.active_connections = []
        self.natiq_instances = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        
        if session_id not in self.natiq_instances:
            self.natiq_instances[session_id] = NatiqSmart()
        
        return self.natiq_instances[session_id]
    
    def disconnect(self, websocket: WebSocket, session_id: str):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

manager = ConnectionManager()

# Routes اصلی
@app.get("/")
async def root():
    html_content = """
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="utf-8">
        <title>natiq-ultimate v2.1</title>
        <style>
            body {
                font-family: sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0;
            }
            .container {
                background: rgba(255,255,255,0.1);
                padding: 40px;
                border-radius: 20px;
                text-align: center;
                backdrop-filter: blur(10px);
                max-width: 600px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                font-size: 2.5em;
                margin-bottom: 20px;
            }
            .status {
                background: rgba(16, 185, 129, 0.2);
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
                border-right: 5px solid #10b981;
            }
            .endpoints {
                text-align: right;
                background: rgba(255,255,255,0.05);
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }
            .btn {
                display: inline-block;
                background: white;
                color: #667eea;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 25px;
                margin: 10px;
                font-weight: bold;
                transition: all 0.3s;
            }
            .btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 natiq-ultimate v2.1</h1>
            <div class="status">
                <h3>✅ سرور فعال است</h3>
                <p>هوش مصنوعی فارسی - نسخه Termux</p>
            </div>
            
            <p>برای استفاده از رابط کاربری کامل، به آدرس زیر بروید:</p>
            <a href="/chat" class="btn">💬 شروع چت</a>
            
            <div class="endpoints">
                <h3>📡 Endpoint‌های API:</h3>
                <ul style="list-style: none; padding-right: 10px;">
                    <li><strong>GET</strong> <a href="/api/health" style="color: #a5b4fc;">/api/health</a> - وضعیت سرور</li>
                    <li><strong>POST</strong> /api/chat/{session_id} - ارسال پیام</li>
                    <li><strong>GET</strong> <a href="/api/test" style="color: #a5b4fc;">/api/test</a> - تست ساده</li>
                    <li><strong>WS</strong> /ws/{session_id} - WebSocket چت</li>
                </ul>
            </div>
            
            <p style="margin-top: 30px; opacity: 0.8; font-size: 0.9em;">
                نسخه ۲.۱ | اجرا شده در Termux
            </p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(html_content)

@app.get("/chat")
async def chat_page():
    # این endpoint صفحه چت ساده‌ای برمی‌گرداند
    return HTMLResponse("""
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="utf-8">
        <title>چت با natiq</title>
        <style>
            body {
                font-family: sans-serif;
                padding: 20px;
                background: #f0f2f5;
            }
            .chat-container {
                max-width: 600px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
            .message {
                margin: 10px 0;
                padding: 10px 15px;
                border-radius: 15px;
                max-width: 80%;
            }
            .bot {
                background: #e3f2fd;
                margin-right: auto;
                border-top-right-radius: 5px;
            }
            .user {
                background: #4f46e5;
                color: white;
                margin-left: auto;
                border-top-left-radius: 5px;
            }
            input {
                width: 100%;
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 25px;
                margin-top: 20px;
                font-size: 16px;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <h2>💬 چت با natiq</h2>
            <div id="messages">
                <div class="message bot">سلام! من natiq هستم. چطور می‌تونم کمک کنم؟</div>
            </div>
            <input type="text" id="input" placeholder="پیام خود را بنویسید... (Enter)">
        </div>
        
        <script>
            const input = document.getElementById('input');
            const messages = document.getElementById('messages');
            
            input.addEventListener('keypress', async (e) => {
                if (e.key === 'Enter' && input.value.trim()) {
                    const text = input.value;
                    input.value = '';
                    
                    // نمایش پیام کاربر
                    const userMsg = document.createElement('div');
                    userMsg.className = 'message user';
                    userMsg.textContent = text;
                    messages.appendChild(userMsg);
                    
                    // ارسال به سرور
                    try {
                        const response = await fetch('/api/chat/test_session', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({message: text})
                        });
                        
                        const data = await response.json();
                        
                        // نمایش پاسخ ربات
                        const botMsg = document.createElement('div');
                        botMsg.className = 'message bot';
                        botMsg.textContent = data.answer;
                        messages.appendChild(botMsg);
                    } catch (error) {
                        const errorMsg = document.createElement('div');
                        errorMsg.className = 'message bot';
                        errorMsg.textContent = 'خطا در ارتباط با سرور';
                        messages.appendChild(errorMsg);
                    }
                }
            });
        </script>
    </body>
    </html>
    """)

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "natiq-ultimate",
        "version": "2.1",
        "natiq_ready": NATIQ_READY,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/test")
async def test():
    return {
        "message": "این یک پیام تست از سرور natiq-ultimate است!",
        "status": "کار می‌کند",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/chat/{session_id}")
async def chat_endpoint(session_id: str, request: dict):
    try:
        question = request.get("message", "")
        
        if not question:
            raise HTTPException(status_code=400, detail="پیام الزامی است")
        
        # ایجاد یا دریافت نمونه natiq
        if session_id not in manager.natiq_instances:
            manager.natiq_instances[session_id] = NatiqSmart()
        
        natiq = manager.natiq_instances[session_id]
        
        # پردازش سوال
        analysis = natiq.analyze_question(question)
        answer = natiq.generate_answer(question, analysis)
        
        # ذخیره گفتگو
        natiq.save_conversation(question, answer)
        
        return {
            "session_id": session_id,
            "question": question,
            "answer": answer,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat(),
            "server": "natiq-ultimate v2.1"
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "message": "خطا در پردازش سوال",
                "timestamp": datetime.now().isoformat()
            }
        )

# WebSocket endpoint
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    
    if session_id not in manager.natiq_instances:
        manager.natiq_instances[session_id] = NatiqSmart()
    
    natiq = manager.natiq_instances[session_id]
    
    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message", data.get("content", ""))
            
            if message:
                analysis = natiq.analyze_question(message)
                answer = natiq.generate_answer(message, analysis)
                
                await websocket.send_json({
                    "type": "response",
                    "response": answer,
                    "analysis": analysis,
                    "timestamp": datetime.now().isoformat()
                })
                
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if websocket in manager.active_connections:
            manager.active_connections.remove(websocket)

# سرویس فایل‌های استاتیک
frontend_dir = current_dir.parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")
    print(f"✅ فایل‌های استاتیک از {frontend_dir} سرو می‌شوند")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 natiq-ultimate v2.1 - سرور اصلی")
    print("="*60)
    print(f"📡 آدرس: http://0.0.0.0:8000")
    print(f"💬 چت: http://localhost:8000/chat")
    print(f"📊 وضعیت: http://localhost:8000/api/health")
    print(f"🧠 natiq آماده: {NATIQ_READY}")
    print("="*60)
    print("برای توقف: Ctrl+C")
    print("="*60 + "\n")
    
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False
    )
