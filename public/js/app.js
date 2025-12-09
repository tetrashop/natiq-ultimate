// ناطق اولتیمیت - رابط کاربری اصلی

class NatiqApp {
    constructor() {
        this.apiBaseUrl = '/api';
        this.sessionId = this.generateSessionId();
        this.conversationHistory = [];
        this.isTyping = false;
        
        this.init();
    }
    
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    async init() {
        this.initUI();
        this.initEventListeners();
        await this.checkSystemStatus();
        this.loadWelcomeMessage();
    }
    
    initUI() {
        // ایجاد رابط چت
        const chatContainer = document.createElement('div');
        chatContainer.className = 'chat-container';
        chatContainer.innerHTML = `
            <div class="chat-header">
                <div class="header-content">
                    <h1><i class="fas fa-brain"></i> ناطق اولتیمیت</h1>
                    <div class="status-indicator">
                        <span class="status-dot" id="statusDot"></span>
                        <span class="status-text" id="statusText">در حال اتصال...</span>
                    </div>
                </div>
            </div>
            
            <div class="chat-messages" id="chatMessages">
                <!-- پیام‌ها اینجا نمایش داده می‌شوند -->
            </div>
            
            <div class="chat-input-container">
                <div class="input-wrapper">
                    <textarea 
                        id="messageInput" 
                        placeholder="پیام خود را اینجا بنویسید... (Enter برای ارسال، Shift+Enter برای خط جدید)"
                        rows="1"
                    ></textarea>
                    <button id="sendButton" class="send-button">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </div>
                <div class="input-info">
                    <span id="charCount">0 کاراکتر</span>
                    <span class="hint">ناطق اولتیمیت نسخه 1.5.0</span>
                </div>
            </div>
            
            <div class="chat-footer">
                <button id="clearChat" class="footer-button">
                    <i class="fas fa-trash"></i> پاکسازی چت
                </button>
                <button id="testOpenAI" class="footer-button">
                    <i class="fas fa-vial"></i> تست اتصال
                </button>
                <button id="exportChat" class="footer-button">
                    <i class="fas fa-download"></i> ذخیره مکالمه
                </button>
            </div>
        `;
        
        document.body.appendChild(chatContainer);
        
        // استایل‌های اضافی
        const style = document.createElement('style');
        style.textContent = `
            * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Vazirmatn', sans-serif; }
            
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            .chat-container {
                width: 100%;
                max-width: 800px;
                height: 90vh;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }
            
            .chat-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px 30px;
            }
            
            .header-content {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .chat-header h1 {
                font-size: 1.5rem;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .status-indicator {
                display: flex;
                align-items: center;
                gap: 10px;
                background: rgba(255,255,255,0.2);
                padding: 8px 15px;
                border-radius: 20px;
                font-size: 0.9rem;
            }
            
            .status-dot {
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: #ccc;
                animation: pulse 2s infinite;
            }
            
            .status-dot.online { background: #2ecc71; }
            .status-dot.offline { background: #e74c3c; }
            
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }
            
            .chat-messages {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            
            .message {
                max-width: 80%;
                padding: 15px;
                border-radius: 15px;
                line-height: 1.6;
                animation: slideIn 0.3s ease;
            }
            
            @keyframes slideIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .message.user {
                align-self: flex-end;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-bottom-right-radius: 5px;
            }
            
            .message.ai {
                align-self: flex-start;
                background: #f5f5f5;
                color: #333;
                border-bottom-left-radius: 5px;
            }
            
            .message.ai.typing {
                background: #e8f4fd;
                font-style: italic;
                color: #666;
            }
            
            .message-header {
                display: flex;
                justify-content: space-between;
                font-size: 0.8rem;
                opacity: 0.7;
                margin-bottom: 5px;
            }
            
            .chat-input-container {
                padding: 20px;
                border-top: 1px solid #eee;
            }
            
            .input-wrapper {
                display: flex;
                gap: 10px;
                margin-bottom: 10px;
            }
            
            textarea {
                flex: 1;
                padding: 15px;
                border: 2px solid #ddd;
                border-radius: 10px;
                resize: none;
                font-size: 1rem;
                transition: all 0.3s;
                max-height: 150px;
            }
            
            textarea:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            
            .send-button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 1.2rem;
                transition: all 0.3s;
            }
            
            .send-button:hover {
                transform: scale(1.05);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
            }
            
            .send-button:disabled {
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }
            
            .input-info {
                display: flex;
                justify-content: space-between;
                font-size: 0.9rem;
                color: #666;
            }
            
            .chat-footer {
                padding: 15px 20px;
                border-top: 1px solid #eee;
                display: flex;
                gap: 10px;
                justify-content: center;
            }
            
            .footer-button {
                padding: 10px 20px;
                border: 2px solid #667eea;
                background: white;
                color: #667eea;
                border-radius: 20px;
                cursor: pointer;
                font-size: 0.9rem;
                transition: all 0.3s;
                display: flex;
                align-items: center;
                gap: 5px;
            }
            
            .footer-button:hover {
                background: #667eea;
                color: white;
            }
            
            .typing-indicator {
                display: flex;
                gap: 5px;
                padding: 10px;
            }
            
            .typing-indicator span {
                width: 8px;
                height: 8px;
                background: #667eea;
                border-radius: 50%;
                animation: bounce 1.4s infinite;
            }
            
            .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
            .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
            
            @keyframes bounce {
                0%, 60%, 100% { transform: translateY(0); }
                30% { transform: translateY(-10px); }
            }
            
            @media (max-width: 768px) {
                .chat-container { height: 100vh; border-radius: 0; }
                .message { max-width: 90%; }
                .footer-button span { display: none; }
                .footer-button { padding: 10px 15px; }
            }
        `;
        
        document.head.appendChild(style);
    }
    
    initEventListeners() {
        const input = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendButton');
        const clearBtn = document.getElementById('clearChat');
        const testBtn = document.getElementById('testOpenAI');
        const exportBtn = document.getElementById('exportChat');
        
        // ارسال با Enter
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // تنظیم ارتفاع خودکار textarea
        input.addEventListener('input', (e) => {
            e.target.style.height = 'auto';
            e.target.style.height = (e.target.scrollHeight) + 'px';
            document.getElementById('charCount').textContent = 
                `${e.target.value.length} کاراکتر`;
        });
        
        sendBtn.addEventListener('click', () => this.sendMessage());
        clearBtn.addEventListener('click', () => this.clearChat());
        testBtn.addEventListener('click', () => this.testOpenAIConnection());
        exportBtn.addEventListener('click', () => this.exportConversation());
    }
    
    async checkSystemStatus() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/status`);
            const data = await response.json();
            
            const statusDot = document.getElementById('statusDot');
            const statusText = document.getElementById('statusText');
            
            if (data.ai.openai_connected) {
                statusDot.className = 'status-dot online';
                statusText.textContent = 'AI متصل ✅';
            } else {
                statusDot.className = 'status-dot offline';
                statusText.textContent = 'حالت جایگزین ⚠️';
            }
            
        } catch (error) {
            console.error('خطا در بررسی وضعیت:', error);
        }
    }
    
    loadWelcomeMessage() {
        const welcomeMessage = "سلام! 👋 به ناطق اولتیمیت خوش آمدید. من یک دستیار هوش مصنوعی فارسی هستم. چطور می‌توانم کمکتان کنم؟";
        this.addMessage(welcomeMessage, 'ai');
    }
    
    addMessage(text, sender) {
        const messagesContainer = document.getElementById('chatMessages');
        
        // حذف نشانگر تایپینگ اگر وجود دارد
        const typingIndicator = messagesContainer.querySelector('.typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const timestamp = new Date().toLocaleTimeString('fa-IR', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        
        messageDiv.innerHTML = `
            <div class="message-header">
                <span>${sender === 'user' ? '👤 شما' : '🤖 ناطق'}</span>
                <span>${timestamp}</span>
            </div>
            <div class="message-content">${this.formatMessage(text)}</div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // ذخیره در تاریخچه
        this.conversationHistory.push({
            text,
            sender,
            timestamp: new Date().toISOString()
        });
    }
    
    showTypingIndicator() {
        const messagesContainer = document.getElementById('chatMessages');
        
        // حذف اگر قبلاً وجود دارد
        const existing = messagesContainer.querySelector('.typing-indicator');
        if (existing) existing.remove();
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message ai typing';
        typingDiv.innerHTML = `
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        `;
        
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    formatMessage(text) {
        // تبدیل لینک‌ها به تگ‌های <a>
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        return text.replace(urlRegex, url => 
            `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`
        ).replace(/\n/g, '<br>');
    }
    
    async sendMessage() {
        const input = document.getElementById('messageInput');
        const message = input.value.trim();
        
        if (!message) return;
        
        // نمایش پیام کاربر
        this.addMessage(message, 'user');
        
        // پاک کردن ورودی
        input.value = '';
        input.style.height = 'auto';
        document.getElementById('charCount').textContent = '0 کاراکتر';
        
        // غیرفعال کردن دکمه ارسال
        const sendBtn = document.getElementById('sendButton');
        sendBtn.disabled = true;
        
        // نمایش نشانگر تایپینگ
        this.showTypingIndicator();
        
        try {
            // ارسال به API
            const startTime = Date.now();
            const response = await fetch(`${this.apiBaseUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });
            
            const data = await response.json();
            const responseTime = Date.now() - startTime;
            
            if (data.success) {
                // نمایش پاسخ AI
                this.addMessage(data.response, 'ai');
                
                // بروزرسانی وضعیت
                await this.checkSystemStatus();
                
            } else {
                throw new Error(data.message || 'خطا در دریافت پاسخ');
            }
            
        } catch (error) {
            console.error('خطا در ارسال پیام:', error);
            this.addMessage('متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید.', 'ai');
        } finally {
            // فعال کردن دکمه ارسال
            sendBtn.disabled = false;
        }
    }
    
    clearChat() {
        if (!confirm('آیا مطمئن هستید که می‌خواهید مکالمه را پاک کنید؟')) {
            return;
        }
        
        const messagesContainer = document.getElementById('chatMessages');
        messagesContainer.innerHTML = '';
        this.conversationHistory = [];
        
        // پاکسازی حافظه سرور
        fetch(`${this.apiBaseUrl}/clear-memory?session_id=${this.sessionId}`, {
            method: 'POST'
        }).catch(console.error);
        
        this.loadWelcomeMessage();
        this.showToast('مکالمه پاکسازی شد', 'success');
    }
    
    async testOpenAIConnection() {
        this.showToast('در حال تست اتصال OpenAI...', 'info');
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/test-openai`);
            const data = await response.json();
            
            if (data.success) {
                this.showToast(`✅ OpenAI متصل است: ${data.test_response}`, 'success');
            } else {
                this.showToast(`⚠️ ${data.message}`, 'warning');
            }
        } catch (error) {
            this.showToast('❌ خطا در تست اتصال', 'error');
        }
    }
    
    exportConversation() {
        const chatData = {
            session_id: this.sessionId,
            timestamp: new Date().toISOString(),
            conversation: this.conversationHistory
        };
        
        const blob = new Blob([JSON.stringify(chatData, null, 2)], { 
            type: 'application/json' 
        });
        
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `natiq-chat-${new Date().getTime()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showToast('مکالمه ذخیره شد', 'success');
    }
    
    showToast(message, type = 'info') {
        // ایجاد toast
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: ${type === 'success' ? '#2ecc71' : type === 'error' ? '#e74c3c' : '#3498db'};
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(toast);
        
        // حذف بعد از 3 ثانیه
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
        
        // اضافه کردن استایل انیمیشن اگر وجود ندارد
        if (!document.querySelector('#toast-animations')) {
            const style = document.createElement('style');
            style.id = 'toast-animations';
            style.textContent = `
                @keyframes slideIn {
                    from { transform: translateX(-100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes slideOut {
                    from { transform: translateX(0); opacity: 1; }
                    to { transform: translateX(-100%); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }
    }
}

// راه‌اندازی اپلیکیشن
document.addEventListener('DOMContentLoaded', () => {
    window.natiqApp = new NatiqApp();
});
