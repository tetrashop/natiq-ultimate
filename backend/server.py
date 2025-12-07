
#!/usr/bin/env python3
"""
سرور اصلی natiq-ultimate - نسخه نهایی برای GitHub و Vercel
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import asyncio
import uuid

# اضافه کردن مسیر backend
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# تلاش برای import natiq_smart
try:
    from natiq_smart import NatiqSmart
    NATIQ_READY = True
except ImportError:
    print("⚠️  ماژول natiq_smart یافت نشد. استفاده از نسخه ساده...")
    # کلاس ساده جایگزین
    class NatiqSmart:
        def __init__(self):
            self.user_name = "کاربر"
            self.stats = {
                "questions_asked": 0,
                "topics_covered": set(),
                "session_start": datetime.now().isoformat()
            }
            self.knowledge = {}
        
        def analyze_question(self, question):
            question_lower = question.lower()
            if "سلام" in question_lower:
                return {"type": "greeting", "topic": "سلام"}
            elif "اسم" in question_lower and "چیه" in question_lower:
                return {"type": "name_query", "topic": "نام"}
            elif "اسم من" in question_lower:
                return {"type": "name_set", "topic": "نام"}
            elif "یاد بگیر" in question_lower:
                return {"type": "learn", "topic": "یادگیری"}
            elif "آمار" in question_lower:
                return {"type": "stats", "topic": "آمار"}
            else:
                return {"type": "general", "topic": "عمومی"}
        
        def generate_answer(self, question, analysis):
            self.stats["questions_asked"] += 1
            
            responses = {
                "greeting": f"سلام {self.user_name}! خوش آمدید. چطور می‌تونم کمک کنم؟",
                "name_query": "من natiq-ultimate هستم، دستیار هوشمند فارسی شما!",
                "name_set": f"سلام {self.user_name}! خوشحالم که شما را می‌شناسم.",
                "learn": "متوجه شدم! برای آموزش از فرمت 'یاد بگیر سوال|پاسخ' استفاده کنید.",
                "stats": f"📊 آمار جلسه:\nسوالات: {self.stats['questions_asked']}\nکاربر: {self.user_name}",
                "general": "متوجه سوال شما شدم. من natiq-ultimate هستم و آماده کمک به شما!"
            }
            
            return responses.get(analysis["type"], "پاسخ پیش‌فرض")
        
        def save_conversation(self, question, answer):
            # ذخیره در حافظه (می‌توانید به فایل هم ذخیره کنید)
            pass
    
    NATIQ_READY = False

app = FastAPI(
    title="natiq-ultimate API",
    description="هوش مصنوعی فارسی پیشرفته",
    version="2.2.0"
)

# CORS برای Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# مدیر WebSocket
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
    """صفحه اصلی - برای Vercel"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="utf-8">
        <title>🤖 natiq-ultimate | هوش مصنوعی فارسی</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="/static/css/style.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    </head>
    <body>
        <div class="container">
            <header class="header">
                <div class="logo">
                    <i class="fas fa-robot"></i>
                    <h1>natiq-ultimate</h1>
                    <span class="version">نسخه ۲.۲</span>
                </div>
                <div class="status">
                    <span class="status-dot" id="statusDot"></span>
                    <span id="statusText">🔗 متصل</span>
                </div>
            </header>
            
            <div class="main-content">
                <div class="chat-container" id="chatContainer">
                    <div class="welcome-message">
                        <div class="message bot">
                            <div class="avatar pulse">
                                <i class="fas fa-robot"></i>
                            </div>
                            <div class="content">
                                <div class="text">
                                    <h3>🚀 natiq-ultimate v2.2</h3>
                                    <p>خوش آمدید! من یک دستیار هوشمند فارسی هستم که روی Vercel مستقر شده‌ام.</p>
                                    <p>می‌توانید با من چت کنید یا با گفتن <code>یاد بگیر سوال|پاسخ</code> به من آموزش دهید.</p>
                                    <p><strong>📡 وضعیت سرور: فعال</strong></p>
                                </div>
                                <div class="time">همین الان</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="sidebar">
                    <div class="sidebar-section">
                        <h3><i class="fas fa-info-circle"></i> اطلاعات</h3>
                        <div class="info-box">
                            <p><i class="fas fa-server"></i> <strong>میزبان:</strong> Vercel</p>
                            <p><i class="fas fa-code"></i> <strong>Backend:</strong> FastAPI + Python</p>
                            <p><i class="fas fa-globe"></i> <strong>Frontend:</strong> HTML5 + CSS3 + JS</p>
                            <p><i class="fas fa-database"></i> <strong>ذخیره‌سازی:</strong> حافظه موقت</p>
                        </div>
                    </div>
                    
                    <div class="sidebar-section">
                        <h3><i class="fas fa-terminal"></i> تست سریع API</h3>
                        <div class="api-test">
                            <button onclick="testHealth()" class="api-btn">
                                <i class="fas fa-heartbeat"></i> تست سلامت
                            </button>
                            <button onclick="testChat()" class="api-btn">
                                <i class="fas fa-comment"></i> تست چت
                            </button>
                            <div id="apiResult" class="api-result"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="input-container">
                <div class="input-wrapper">
                    <input type="text" id="messageInput" placeholder="سوال خود را بنویسید..." autocomplete="off">
                    <button id="sendButton">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </div>
                <div class="quick-actions">
                    <button class="quick-btn" onclick="sendQuick('سلام')">
                        <i class="fas fa-hand"></i> سلام
                    </button>
                    <button class="quick-btn" onclick="sendQuick('آمار')">
                        <i class="fas fa-chart-bar"></i> آمار
                    </button>
                    <button class="quick-btn" onclick="sendQuick('اسم من چیست؟')">
                        <i class="fas fa-user"></i> نام من
                    </button>
                </div>
            </div>
        </div>
        
        <script src="/static/js/app.js"></script>
        <script>
            function sendQuick(text) {
                document.getElementById('messageInput').value = text;
                document.getElementById('sendButton').click();
            }
            
            async function testHealth() {
                const result = document.getElementById('apiResult');
                result.innerHTML = '<div class="loading">در حال تست...</div>';
                
                try {
                    const response = await fetch('/api/health');
                    const data = await response.json();
                    result.innerHTML = `<div class="success">✅ سلامت سرور: ${data.status}<br>نسخه: ${data.version}</div>`;
                } catch (error) {
                    result.innerHTML = `<div class="error">❌ خطا در تست: ${error.message}</div>`;
                }
            }
            
            async function testChat() {
                const result = document.getElementById('apiResult');
                result.innerHTML = '<div class="loading">در حال تست چت...</div>';
                
                try {
                    const response = await fetch('/api/chat/test_session', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({message: 'سلام تست'})
                    });
                    const data = await response.json();
                    result.innerHTML = `<div class="success">✅ تست چت موفق:<br>"${data.answer}"</div>`;
                } catch (error) {
                    result.innerHTML = `<div class="error">❌ خطا در تست چت: ${error.message}</div>`;
                }
            }
        </script>
    </body>
    </html>
    """)

@app.get("/api/health")
async def health_check():
    """بررسی سلامت - ضروری برای Vercel"""
    return {
        "status": "healthy",
        "service": "natiq-ultimate",
        "version": "2.2.0",
        "environment": os.getenv("VERCEL_ENV", "development"),
        "region": os.getenv("VERCEL_REGION", "local"),
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            {"path": "/", "method": "GET", "description": "صفحه اصلی"},
            {"path": "/api/health", "method": "GET", "description": "سلامت سرور"},
            {"path": "/api/chat/{session_id}", "method": "POST", "description": "ارسال پیام"},
            {"path": "/ws/{session_id}", "method": "WS", "description": "WebSocket چت"}
        ]
    }

@app.post("/api/chat/{session_id}")
async def chat_endpoint(session_id: str, request: dict):
    """پایان‌ده چت - برای Vercel"""
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
            "environment": "vercel"
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

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket برای چت بلادرنگ"""
    await websocket.accept()
    
    if session_id not in manager.natiq_instances:
        manager.natiq_instances[session_id] = NatiqSmart()
    
    natiq = manager.natiq_instances[session_id]
    
    try:
        while True:
            data = await websocket.receive_json()
            message_type = data.get("type", "message")
            
            if message_type == "message":
                message = data.get("content", "")
                
                if message:
                    analysis = natiq.analyze_question(message)
                    answer = natiq.generate_answer(message, analysis)
                    
                    await websocket.send_json({
                        "type": "response",
                        "content": answer,
                        "analysis": analysis,
                        "timestamp": datetime.now().isoformat()
                    })
            
            elif message_type == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, session_id)

# سرویس فایل‌های استاتیک برای Vercel
frontend_dir = current_dir.parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

# برای Vercel نیاز به export app داریم
app = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
