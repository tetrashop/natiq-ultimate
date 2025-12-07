#!/usr/bin/env python3
"""
سرور natiq-ultimate - نسخه ساده و صحیح برای Vercel
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import os
from datetime import datetime
import json

app = FastAPI(
    title="natiq-ultimate",
    description="هوش مصنوعی فارسی",
    version="2.4.0"
)

# CORS برای Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# کلاس ساده Natiq
class NatiqSmart:
    def __init__(self):
        self.user_name = "کاربر"
        self.stats = {"questions_asked": 0}
    
    def analyze_question(self, question):
        question_lower = question.lower()
        if "سلام" in question_lower:
            return {"type": "greeting", "topic": "سلام"}
        elif "اسم" in question_lower:
            return {"type": "name", "topic": "نام"}
        elif "آمار" in question_lower:
            return {"type": "stats", "topic": "آمار"}
        else:
            return {"type": "general", "topic": "عمومی"}
    
    def generate_answer(self, question, analysis):
        self.stats["questions_asked"] += 1
        
        if analysis["type"] == "greeting":
            return f"سلام {self.user_name}! خوش آمدید. من natiq-ultimate هستم. 🤖"
        elif analysis["type"] == "name":
            return "من natiq-ultimate هستم، دستیار هوشمند فارسی شما!"
        elif analysis["type"] == "stats":
            return f"📊 آمار: {self.stats['questions_asked']} سوال پاسخ داده شده"
        else:
            return f"سوال جالبی پرسیدید: '{question}'. من در حال یادگیری هستم!"

# صفحه اصلی با HTML کامل
@app.get("/")
async def root():
    html_content = """
    <!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🤖 natiq-ultimate | هوش مصنوعی فارسی</title>
        <style>
            /* Reset */
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
                line-height: 1.6;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                min-height: 100vh;
                box-shadow: 0 0 40px rgba(0,0,0,0.1);
            }
            
            /* Header */
            .header {
                background: linear-gradient(90deg, #4f46e5, #7c3aed);
                color: white;
                padding: 25px 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .logo {
                display: flex;
                align-items: center;
                gap: 20px;
            }
            
            .logo i {
                font-size: 3em;
            }
            
            .logo h1 {
                font-size: 2em;
                font-weight: 700;
            }
            
            .version {
                background: rgba(255,255,255,0.2);
                padding: 5px 15px;
                border-radius: 15px;
                font-size: 0.9em;
            }
            
            .status {
                display: flex;
                align-items: center;
                gap: 12px;
                background: rgba(255,255,255,0.1);
                padding: 10px 25px;
                border-radius: 25px;
            }
            
            .status-dot {
                width: 12px;
                height: 12px;
                background: #4ade80;
                border-radius: 50%;
                animation: blink 1.5s infinite;
            }
            
            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.3; }
            }
            
            /* Main Content */
            .main-content {
                display: flex;
                min-height: 70vh;
            }
            
            .chat-area {
                flex: 1;
                padding: 40px;
                background: #f8fafc;
                display: flex;
                flex-direction: column;
            }
            
            .messages {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
                background: white;
                border-radius: 15px;
                box-shadow: inset 0 0 10px rgba(0,0,0,0.05);
                margin-bottom: 30px;
            }
            
            .message {
                margin: 15px 0;
                padding: 15px 20px;
                border-radius: 15px;
                max-width: 80%;
            }
            
            .bot-message {
                background: #e3f2fd;
                margin-right: auto;
                border-top-right-radius: 5px;
            }
            
            .user-message {
                background: #4f46e5;
                color: white;
                margin-left: auto;
                border-top-left-radius: 5px;
            }
            
            /* Input Area */
            .input-area {
                background: white;
                padding: 25px;
                border-top: 1px solid #e5e7eb;
            }
            
            .input-group {
                display: flex;
                gap: 15px;
                margin-bottom: 20px;
            }
            
            #messageInput {
                flex: 1;
                padding: 18px 25px;
                border: 2px solid #e5e7eb;
                border-radius: 25px;
                font-size: 1.1em;
                font-family: inherit;
            }
            
            #messageInput:focus {
                outline: none;
                border-color: #4f46e5;
                box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
            }
            
            #sendButton {
                width: 70px;
                background: linear-gradient(45deg, #4f46e5, #7c3aed);
                color: white;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 1.3em;
                transition: all 0.3s;
            }
            
            #sendButton:hover {
                transform: scale(1.05);
                box-shadow: 0 5px 20px rgba(79, 70, 229, 0.3);
            }
            
            .quick-buttons {
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .quick-btn {
                padding: 12px 25px;
                background: #f3f4f6;
                border: 1px solid #e5e7eb;
                border-radius: 20px;
                cursor: pointer;
                transition: all 0.3s;
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 1em;
            }
            
            .quick-btn:hover {
                background: #e5e7eb;
                transform: translateY(-2px);
            }
            
            /* Sidebar */
            .sidebar {
                width: 350px;
                background: #f9fafb;
                border-left: 1px solid #e5e7eb;
                padding: 40px 30px;
            }
            
            .sidebar-section {
                margin-bottom: 35px;
                padding-bottom: 25px;
                border-bottom: 1px solid #e5e7eb;
            }
            
            .sidebar-section h3 {
                display: flex;
                align-items: center;
                gap: 15px;
                margin-bottom: 20px;
                color: #374151;
                font-size: 1.2em;
            }
            
            /* Responsive */
            @media (max-width: 768px) {
                .container {
                    margin: 0;
                }
                
                .main-content {
                    flex-direction: column;
                }
                
                .sidebar {
                    width: 100%;
                    border-left: none;
                    border-top: 1px solid #e5e7eb;
                }
                
                .header {
                    padding: 20px;
                    flex-direction: column;
                    gap: 15px;
                    text-align: center;
                }
                
                .logo {
                    flex-direction: column;
                    gap: 10px;
                }
                
                .message {
                    max-width: 90%;
                }
                
                .input-group {
                    flex-direction: column;
                }
                
                #sendButton {
                    width: 100%;
                    height: 60px;
                }
            }
            
            /* Welcome Message */
            .welcome {
                background: linear-gradient(45deg, #e3f2fd, #bbdefb);
                padding: 30px;
                border-radius: 20px;
                margin-bottom: 30px;
                border-right: 5px solid #2196f3;
            }
            
            .welcome h2 {
                color: #1565c0;
                margin-bottom: 15px;
            }
            
            .welcome ul {
                padding-right: 20px;
                margin: 15px 0;
            }
            
            .welcome li {
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
        </style>
        
        <!-- Font Awesome -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        
        <!-- Google Fonts -->
        <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        
        <script>
            class NatiqApp {
                constructor() {
                    this.sessionId = 'session_' + Date.now();
                    this.baseUrl = window.location.origin;
                    this.init();
                }
                
                init() {
                    console.log('🚀 natiq-ultimate شروع شد');
                    this.setupEventListeners();
                    this.updateStatus('✅ متصل');
                    
                    // تست خودکار اتصال
                    this.testConnection();
                }
                
                setupEventListeners() {
                    // دکمه ارسال
                    const sendBtn = document.getElementById('sendButton');
                    const messageInput = document.getElementById('messageInput');
                    
                    sendBtn.addEventListener('click', () => this.sendMessage());
                    
                    messageInput.addEventListener('keypress', (e) => {
                        if (e.key === 'Enter') {
                            e.preventDefault();
                            this.sendMessage();
                        }
                    });
                    
                    // دکمه‌های سریع
                    document.querySelectorAll('.quick-btn').forEach(btn => {
                        btn.addEventListener('click', (e) => {
                            const text = e.target.getAttribute('data-question') || 
                                       e.target.closest('.quick-btn').getAttribute('data-question');
                            if (text) {
                                messageInput.value = text;
                                this.sendMessage();
                            }
                        });
                    });
                }
                
                async testConnection() {
                    try {
                        const response = await fetch(this.baseUrl + '/api/health');
                        if (response.ok) {
                            console.log('✅ اتصال موفق');
                            return true;
                        }
                    } catch (error) {
                        console.warn('⚠️ اتصال ناموفق');
                    }
                    return false;
                }
                
                updateStatus(message) {
                    const statusText = document.getElementById('statusText');
                    if (statusText) {
                        statusText.textContent = message;
                    }
                }
                
                async sendMessage() {
                    const messageInput = document.getElementById('messageInput');
                    const message = messageInput.value.trim();
                    
                    if (!message) return;
                    
                    // نمایش پیام کاربر
                    this.addMessage(message, 'user');
                    messageInput.value = '';
                    
                    // نمایش تایپینگ
                    this.showTyping();
                    
                    try {
                        // ارسال به سرور
                        const response = await fetch(this.baseUrl + '/api/chat/' + this.sessionId, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ message: message })
                        });
                        
                        if (!response.ok) {
                            throw new Error(`HTTP error: ${response.status}`);
                        }
                        
                        const data = await response.json();
                        
                        // پنهان کردن تایپینگ
                        this.hideTyping();
                        
                        // نمایش پاسخ
                        this.addMessage(data.answer, 'bot');
                        
                        this.updateStatus('✅ پاسخ دریافت شد');
                        
                    } catch (error) {
                        this.hideTyping();
                        console.error('❌ خطا:', error);
                        
                        this.addMessage('خطا در ارتباط با سرور. لطفاً دوباره تلاش کنید.', 'error');
                        this.updateStatus('❌ خطا در ارتباط');
                    }
                }
                
                addMessage(text, type) {
                    const messagesDiv = document.getElementById('messages');
                    const time = new Date().toLocaleTimeString('fa-IR', {
                        hour: '2-digit',
                        minute: '2-digit'
                    });
                    
                    const messageDiv = document.createElement('div');
                    messageDiv.className = `message ${type === 'user' ? 'user-message' : 'bot-message'}`;
                    
                    messageDiv.innerHTML = `
                        <div style="display: flex; align-items: flex-start; gap: 10px;">
                            <div style="font-size: 1.5em;">
                                ${type === 'user' ? '👤' : '🤖'}
                            </div>
                            <div style="flex: 1;">
                                <div>${this.escapeHtml(text)}</div>
                                <div style="font-size: 0.8em; opacity: 0.7; margin-top: 5px;">${time}</div>
                            </div>
                        </div>
                    `;
                    
                    messagesDiv.appendChild(messageDiv);
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }
                
                showTyping() {
                    const messagesDiv = document.getElementById('messages');
                    
                    const typingDiv = document.createElement('div');
                    typingDiv.className = 'message bot-message';
                    typingDiv.id = 'typingIndicator';
                    typingDiv.innerHTML = `
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <div>🤖</div>
                            <div style="display: flex; gap: 5px;">
                                <span style="animation: blink 1.4s infinite;">●</span>
                                <span style="animation: blink 1.4s infinite 0.2s;">●</span>
                                <span style="animation: blink 1.4s infinite 0.4s;">●</span>
                            </div>
                        </div>
                    `;
                    
                    messagesDiv.appendChild(typingDiv);
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }
                
                hideTyping() {
                    const typing = document.getElementById('typingIndicator');
                    if (typing) {
                        typing.remove();
                    }
                }
                
                escapeHtml(text) {
                    const div = document.createElement('div');
                    div.textContent = text;
                    return div.innerHTML;
                }
            }
            
            // راه‌اندازی اپ
            document.addEventListener('DOMContentLoaded', () => {
                window.natiqApp = new NatiqApp();
                document.getElementById('messageInput').focus();
            });
        </script>
    </head>
    <body>
        <div class="container">
            <!-- هدر -->
            <header class="header">
                <div class="logo">
                    <i class="fas fa-robot"></i>
                    <div>
                        <h1>natiq-ultimate</h1>
                        <span class="version">نسخه ۲.۴</span>
                    </div>
                </div>
                <div class="status">
                    <span class="status-dot"></span>
                    <span id="statusText">در حال اتصال...</span>
                </div>
            </header>
            
            <!-- محتوای اصلی -->
            <div class="main-content">
                <!-- قسمت چت -->
                <div class="chat-area">
                    <div class="messages" id="messages">
                        <!-- پیام خوش‌آمدگویی -->
                        <div class="welcome">
                            <h2>🚀 خوش آمدید به natiq-ultimate!</h2>
                            <p>من یک دستیار هوشمند فارسی هستم که روی <strong>Vercel</strong> مستقر شده‌ام.</p>
                            <p><strong>✨ می‌توانم:</strong></p>
                            <ul>
                                <li><i class="fas fa-comment"></i> به سوالات فارسی پاسخ دهم</li>
                                <li><i class="fas fa-brain"></i> از گفتگو با شما یاد بگیرم</li>
                                <li><i class="fas fa-chart-bar"></i> آمار گفتگو را نگه دارم</li>
                                <li><i class="fas fa-bolt"></i> سریع و کارآمد پاسخ دهم</li>
                            </ul>
                            <p><strong>💡 نکته:</strong> سوال خود را در کادر زیر بنویسید یا از دکمه‌های سریع استفاده کنید.</p>
                        </div>
                    </div>
                    
                    <!-- ورودی -->
                    <div class="input-area">
                        <div class="input-group">
                            <input 
                                type="text" 
                                id="messageInput" 
                                placeholder="سوال خود را اینجا بنویسید..." 
                                autocomplete="off"
                                autofocus
                            >
                            <button id="sendButton">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                        
                        <div class="quick-buttons">
                            <button class="quick-btn" data-question="سلام">
                                <i class="fas fa-hand"></i> سلام
                            </button>
                            <button class="quick-btn" data-question="اسم تو چیست؟">
                                <i class="fas fa-robot"></i> اسم تو
                            </button>
                            <button class="quick-btn" data-question="آمار این جلسه">
                                <i class="fas fa-chart-bar"></i> آمار
                            </button>
                            <button class="quick-btn" data-question="چگونه کار می‌کنی؟">
                                <i class="fas fa-cogs"></i> نحوه کار
                            </button>
                            <button class="quick-btn" data-question="چه کاری می‌توانی انجام دهی؟">
                                <i class="fas fa-list"></i> قابلیت‌ها
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- سایدبار -->
                <div class="sidebar">
                    <div class="sidebar-section">
                        <h3><i class="fas fa-info-circle"></i> اطلاعات سیستم</h3>
                        <div>
                            <p><strong>🌐 محیط:</strong> Vercel</p>
                            <p><strong>🚀 وضعیت:</strong> فعال</p>
                            <p><strong>📅 زمان:</strong> <span id="currentTime">--:--</span></p>
                            <p><strong>🔗 شناسه:</strong> <span id="sessionDisplay">...</span></p>
                        </div>
                    </div>
                    
                    <div class="sidebar-section">
                        <h3><i class="fas fa-terminal"></i> تست اتصال</h3>
                        <div>
                            <button onclick="testApi()" style="width:100%; padding:12px; background:#4f46e5; color:white; border:none; border-radius:8px; cursor:pointer; margin-bottom:10px;">
                                <i class="fas fa-heartbeat"></i> تست سلامت API
                            </button>
                            <button onclick="clearChat()" style="width:100%; padding:12px; background:#ef4444; color:white; border:none; border-radius:8px; cursor:pointer;">
                                <i class="fas fa-trash"></i> پاک کردن چت
                            </button>
                            <div id="testResult" style="margin-top:15px; padding:10px; border-radius:8px; display:none;"></div>
                        </div>
                    </div>
                    
                    <div class="sidebar-section">
                        <h3><i class="fas fa-code"></i> درباره</h3>
                        <div>
                            <p><strong>natiq-ultimate</strong> یک پروژه هوش مصنوعی فارسی است که با FastAPI ساخته شده و روی Vercel مستقر شده است.</p>
                            <p>هدف: ایجاد یک دستیار هوشمند فارسی قابل دسترسی برای همه.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            // نمایش زمان جاری
            function updateTime() {
                const now = new Date();
                const timeStr = now.toLocaleTimeString('fa-IR');
                document.getElementById('currentTime').textContent = timeStr;
            }
            
            // نمایش شناسه جلسه
            document.getElementById('sessionDisplay').textContent = 
                window.natiqApp.sessionId.substring(0, 15) + '...';
            
            // تست API
            async function testApi() {
                const resultDiv = document.getElementById('testResult');
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = '<div style="color:#f59e0b;">⏳ در حال تست...</div>';
                
                try {
                    const response = await fetch(window.natiqApp.baseUrl + '/api/health');
                    const data = await response.json();
                    
                    resultDiv.innerHTML = `
                        <div style="background:#d1fae5; color:#065f46; padding:10px; border-radius:6px;">
                            <strong>✅ تست موفق</strong><br>
                            وضعیت: ${data.status}<br>
                            نسخه: ${data.version}<br>
                            زمان: ${new Date(data.timestamp).toLocaleTimeString('fa-IR')}
                        </div>
                    `;
                } catch (error) {
                    resultDiv.innerHTML = `
                        <div style="background:#fee2e2; color:#7f1d1d; padding:10px; border-radius:6px;">
                            <strong>❌ خطا در تست</strong><br>
                            ${error.message}
                        </div>
                    `;
                }
                
                setTimeout(() => {
                    resultDiv.style.display = 'none';
                }, 5000);
            }
            
            // پاک کردن چت
            function clearChat() {
                if (confirm('آیا مطمئن هستید که می‌خواهید همه گفتگو را پاک کنید؟')) {
                    const messagesDiv = document.getElementById('messages');
                    const welcomeDiv = messagesDiv.querySelector('.welcome');
                    
                    // حذف همه پیام‌ها به جز پیام خوش‌آمدگویی
                    while (messagesDiv.firstChild) {
                        messagesDiv.removeChild(messagesDiv.firstChild);
                    }
                    
                    // اضافه کردن مجدد پیام خوش‌آمدگویی
                    if (welcomeDiv) {
                        messagesDiv.appendChild(welcomeDiv);
                    } else {
                        // اگر پیام خوش‌آمدگویی نبود، ایجاد کنیم
                        const welcomeMsg = document.createElement('div');
                        welcomeMsg.className = 'welcome';
                        welcomeMsg.innerHTML = `
                            <h2>🚀 گفتگو پاک شد!</h2>
                            <p>همه پیام‌ها حذف شدند. می‌توانید دوباره شروع کنید.</p>
                        `;
                        messagesDiv.appendChild(welcomeMsg);
                    }
                    
                    window.natiqApp.updateStatus('✅ گفتگو پاک شد');
                }
            }
            
            // بروزرسانی زمان هر ثانیه
            setInterval(updateTime, 1000);
            updateTime();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html_content)

# API Endpoints
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "natiq-ultimate",
        "version": "2.4.0",
        "environment": "vercel",
        "timestamp": datetime.now().isoformat(),
        "message": "سرور به درستی کار می‌کند"
    }

@app.post("/api/chat/{session_id}")
async def chat_endpoint(session_id: str, request: dict):
    try:
        question = request.get("message", "")
        
        if not question:
            raise HTTPException(status_code=400, detail="پیام الزامی است")
        
        natiq = NatiqSmart()
        analysis = natiq.analyze_question(question)
        answer = natiq.generate_answer(question, analysis)
        
        return {
            "session_id": session_id,
            "question": question,
            "answer": answer,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat(),
            "server": "vercel"
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

# هندلر برای favicon.ico (برای جلوگیری از خطاهای 404)
@app.get("/favicon.ico")
async def favicon():
    return JSONResponse({"status": "no favicon"})

# برای Vercel
app = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
