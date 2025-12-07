#!/usr/bin/env python3
"""
سرور اصلی natiq-ultimate برای Termux
نسخه سبک و سازگار
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import json
import asyncio
import uuid
from datetime import datetime
from pathlib import Path
import sys
import os

# اضافه کردن مسیر backend به sys.path
sys.path.append(str(Path(__file__).parent))

try:
    from natiq_smart import NatiqSmart
    NATIQ_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  خطا در بارگیری natiq_smart: {e}")
    print("📦 در حال ایجاد نسخه جایگزین...")
    NATIQ_AVAILABLE = False
    
    # کلاس جایگزین ساده
    class NatiqSmart:
        def __init__(self):
            self.user_name = "کاربر"
            self.stats = {
                "questions_asked": 0,
                "topics_covered": set(),
                "session_start": datetime.now().isoformat()
            }
        
        def analyze_question(self, question):
            return {"type": "general", "topic": "عمومی"}
        
        def generate_answer(self, question, analysis):
            self.stats["questions_asked"] += 1
            return f"پاسخ به: {question}\n\nمن natiq-ultimate هستم. سیستم در حال راه‌اندازی است."
        
        def save_conversation(self, question, answer):
            pass

# ایجاد برنامه FastAPI
app = FastAPI(
    title="natiq-ultimate API",
    description="هوش مصنوعی فارسی پیشرفته - نسخه Termux",
    version="2.0.0"
)

# CORS middleware - ساده‌تر برای Termux
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# مدیر اتصال WebSocket ساده
class SimpleConnectionManager:
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

manager = SimpleConnectionManager()

# Routes پایه
@app.get("/")
async def root():
    """صفحه اصلی"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="utf-8">
        <title>natiq-ultimate | Termux</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
            h1 {
                margin-bottom: 20px;
            }
            .btn {
                display: inline-block;
                padding: 10px 20px;
                background: white;
                color: #667eea;
                text-decoration: none;
                border-radius: 10px;
                margin: 10px;
                font-weight: bold;
            }
            .status {
                margin-top: 20px;
                padding: 10px;
                background: rgba(255,255,255,0.2);
                border-radius: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 natiq-ultimate</h1>
            <p>هوش مصنوعی فارسی - نسخه Termux</p>
            
            <div style="margin: 20px 0;">
                <a href="/chat" class="btn">💬 شروع چت</a>
                <a href="/api/health" class="btn">📊 وضعیت سرور</a>
            </div>
            
            <div class="status">
                <p>📡 سرور فعال</p>
                <p>🔗 آدرس: http://localhost:8000</p>
            </div>
            
            <p style="margin-top: 30px; font-size: 12px; opacity: 0.8;">
                نسخه ۲.۰ | سازگار با Termux
            </p>
        </div>
    </body>
    </html>
    """)

@app.get("/chat")
async def chat_page():
    """صفحه چت"""
    html_content = """
    <!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>💬 چت با natiq</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: sans-serif;
                background: #f0f2f5;
                height: 100vh;
            }
            .header {
                background: linear-gradient(90deg, #4f46e5, #7c3aed);
                color: white;
                padding: 15px;
                text-align: center;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
            }
            .chat-container {
                padding: 20px;
                height: calc(100vh - 140px);
                overflow-y: auto;
            }
            .message {
                margin: 10px 0;
                display: flex;
                gap: 10px;
            }
            .message.user {
                flex-direction: row-reverse;
            }
            .message.bot .avatar {
                background: #10b981;
            }
            .message.user .avatar {
                background: #3b82f6;
            }
            .avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                flex-shrink: 0;
            }
            .content {
                background: white;
                padding: 10px 15px;
                border-radius: 15px;
                max-width: 70%;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .message.user .content {
                background: #3b82f6;
                color: white;
                border-top-right-radius: 5px;
            }
            .message.bot .content {
                border-top-left-radius: 5px;
            }
            .input-container {
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: white;
                padding: 15px;
                border-top: 1px solid #ddd;
                display: flex;
                gap: 10px;
            }
            #messageInput {
                flex: 1;
                padding: 10px 15px;
                border: 2px solid #e5e7eb;
                border-radius: 25px;
                font-size: 16px;
            }
            #sendButton {
                background: #4f46e5;
                color: white;
                border: none;
                padding: 0 20px;
                border-radius: 25px;
                cursor: pointer;
            }
            .welcome {
                text-align: center;
                padding: 20px;
                background: white;
                border-radius: 15px;
                margin: 20px 0;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            .typing {
                display: flex;
                gap: 5px;
                padding: 10px;
            }
            .typing span {
                width: 8px;
                height: 8px;
                background: #666;
                border-radius: 50%;
                animation: bounce 1.4s infinite;
            }
            .typing span:nth-child(2) { animation-delay: 0.2s; }
            .typing span:nth-child(3) { animation-delay: 0.4s; }
            @keyframes bounce {
                0%, 60%, 100% { transform: translateY(0); }
                30% { transform: translateY(-10px); }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div style="font-size: 24px;">🤖</div>
            <div>
                <h2>natiq-ultimate</h2>
                <small>چت هوشمند فارسی</small>
            </div>
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="welcome">
                <h3>سلام! 👋</h3>
                <p>من natiq-ultimate هستم، دستیار فارسی شما.</p>
                <p>می‌توانید با من چت کنید یا با گفتن "یاد بگیر سوال|پاسخ" به من آموزش دهید.</p>
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="messageInput" placeholder="پیام خود را بنویسید...">
            <button id="sendButton">➤</button>
        </div>
        
        <script>
            const chatContainer = document.getElementById('chatContainer');
            const messageInput = document.getElementById('messageInput');
            const sendButton = document.getElementById('sendButton');
            let sessionId = 'session_' + Date.now();
            
            function addMessage(text, isUser = false) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
                
                messageDiv.innerHTML = `
                    <div class="avatar">${isUser ? '👤' : '🤖'}</div>
                    <div class="content">${text}</div>
                `;
                
                chatContainer.appendChild(messageDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
            
            function showTyping() {
                const typingDiv = document.createElement('div');
                typingDiv.className = 'message bot';
                typingDiv.id = 'typingIndicator';
                typingDiv.innerHTML = `
                    <div class="avatar">🤖</div>
                    <div class="content typing">
                        <span></span><span></span><span></span>
                    </div>
                `;
                chatContainer.appendChild(typingDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
            
            function hideTyping() {
                const typing = document.getElementById('typingIndicator');
                if (typing) typing.remove();
            }
            
            async function sendMessage() {
                const text = messageInput.value.trim();
                if (!text) return;
                
                addMessage(text, true);
                messageInput.value = '';
                showTyping();
                
                try {
                    const response = await fetch(`/api/chat/${sessionId}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: text })
                    });
                    
                    const data = await response.json();
                    hideTyping();
                    addMessage(data.answer);
                } catch (error) {
                    hideTyping();
                    addMessage('⚠️ خطا در ارتباط با سرور');
                    console.error(error);
                }
            }
            
            sendButton.addEventListener('click', sendMessage);
            messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') sendMessage();
            });
            
            // فوکوس روی ورودی
            messageInput.focus();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html_content)

@app.get("/api/health")
async def health_check():
    """بررسی سلامت سرور"""
    return {
        "status": "healthy",
        "service": "natiq-ultimate",
        "version": "2.0.0",
        "platform": "termux",
        "natiq_available": NATIQ_AVAILABLE,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/test")
async def test_endpoint():
    """تست ساده"""
    return {
        "message": "سرور فعال است!",
        "endpoints": {
            "/": "صفحه اصلی",
            "/chat": "صفحه چت",
            "/api/health": "سلامت سرور",
            "/api/test": "این صفحه",
            "/api/chat/{session_id}": "ارسال پیام (POST)"
        }
    }

@app.post("/api/chat/{session_id}")
async def chat_endpoint(session_id: str, request: dict):
    """پردازش پیام - نسخه ساده"""
    question = request.get("message", "")
    
    if not question:
        raise HTTPException(status_code=400, detail="پیام الزامی است")
    
    # ایجاد یا بازیابی نمونه natiq
    if session_id not in manager.natiq_instances:
        manager.natiq_instances[session_id] = NatiqSmart()
    
    natiq = manager.natiq_instances[session_id]
    
    try:
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
            "user": natiq.user_name
        }
    except Exception as e:
        return {
            "session_id": session_id,
            "question": question,
            "answer": f"⚠️ خطا در پردازش: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

# WebSocket ساده‌تر
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """اتصال WebSocket ساده"""
    await websocket.accept()
    
    if session_id not in manager.natiq_instances:
        manager.natiq_instances[session_id] = NatiqSmart()
    
    natiq = manager.natiq_instances[session_id]
    
    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message", "")
            
            if message:
                # پردازش ساده
                if "سلام" in message:
                    response = f"سلام {natiq.user_name}! چطور می‌تونم کمک کنم؟"
                elif "اسم" in message and "چیه" in message:
                    response = "من natiq-ultimate هستم! 🤖"
                elif "یاد بگیر" in message:
                    response = "می‌تونم یاد بگیرم! فرمت: یاد بگیر سوال|پاسخ"
                else:
                    response = f"پیام شما: '{message}'\n\nمن natiq-ultimate هستم. در حال یادگیری هستم!"
                
                await websocket.send_json({
                    "response": response,
                    "timestamp": datetime.now().isoformat()
                })
    
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        manager.disconnect(websocket, session_id)

# سرویس فایل‌های استاتیک (اگر وجود داشته باشند)
static_dir = Path("frontend")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

# اجرای سرور
if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*50)
    print("🤖 natiq-ultimate v2.0 - Termux Edition")
    print("="*50)
    print(f"📡 سرور در حال راه‌اندازی...")
    print(f"🌐 آدرس: http://localhost:8000")
    print(f"💬 چت: http://localhost:8000/chat")
    print(f"📊 وضعیت: http://localhost:8000/api/health")
    print("="*50)
    print("برای توقف: Ctrl+C")
    print("="*50 + "\n")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=False,  # در Termux reload را غیرفعال می‌کنیم
        log_level="info"
    )
