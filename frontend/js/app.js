/**
 * natiq-ultimate v2.1 - رابط کاربری پیشرفته
 * قابلیت عیب‌یابی داخلی و مدیریت اتصال
 */

class NatiqUltimateUI {
    constructor() {
        this.sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        this.ws = null;
        this.isConnected = false;
        this.reconnectTimer = null;
        this.reconnectCount = 0;
        this.maxReconnect = 5;
        
        // ذخیره مکالمات در localStorage
        this.conversations = JSON.parse(localStorage.getItem('natiq_conversations')) || [];
        this.messageCount = parseInt(localStorage.getItem('natiq_message_count')) || 0;
        
        // عناصر DOM
        this.elements = {
            chatContainer: document.getElementById('chatContainer'),
            messageInput: document.getElementById('messageInput'),
            sendButton: document.getElementById('sendButton'),
            connectionAlert: document.getElementById('connectionAlert'),
            alertText: document.getElementById('alertText'),
            retryBtn: document.getElementById('retryBtn'),
            statQuestions: document.getElementById('statQuestions'),
            statTopics: document.getElementById('statTopics'),
            sessionId: document.getElementById('sessionId'),
            sidebarStatus: document.getElementById('sidebarStatus'),
            debugPanel: document.getElementById('debugPanel'),
            debugContent: document.getElementById('debugContent'),
            closeDebug: document.getElementById('closeDebug')
        };
        
        // سیستم لاگ داخلی
        this.logs = [];
        
        this.init();
    }
    
    init() {
        this.log('سیستم رابط کاربری راه‌اندازی شد', 'info');
        this.loadTheme();
        this.setupEventListeners();
        this.updateStats();
        this.connectWebSocket();
        this.displaySessionId();
        
        // بارگیری مکالمات قبلی
        this.loadPreviousConversations();
        
        // تست اولیه اتصال
        this.testConnection();
    }
    
    log(message, type = 'info') {
        const time = new Date().toLocaleTimeString('fa-IR');
        const logEntry = {
            time,
            message,
            type,
            timestamp: Date.now()
        };
        
        this.logs.push(logEntry);
        
        // نمایش در پنل دیباگ
        const logDiv = document.createElement('div');
        logDiv.className = `log-entry ${type}`;
        logDiv.innerHTML = `
            <span class="log-time">[${time}]</span> ${message}
        `;
        
        this.elements.debugContent.appendChild(logDiv);
        this.elements.debugContent.scrollTop = this.elements.debugContent.scrollHeight;
        
        // ذخیره در کنسول (برای توسعه)
        console.log(`[${type.toUpperCase()}] ${message}`);
        
        // اگر خطا است، به کاربر هم نشان بده
        if (type === 'error') {
            this.showUserAlert(message, type);
        }
    }
    
    setupEventListeners() {
        // ارسال پیام
        this.elements.sendButton.addEventListener('click', () => this.sendMessage());
        this.elements.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // تلاش مجدد اتصال
        this.elements.retryBtn.addEventListener('click', () => {
            this.log('تلاش مجدد اتصال به صورت دستی', 'info');
            this.reconnectWebSocket();
        });
        
        // دکمه‌های پیشنهادی
        document.querySelectorAll('.suggestion-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const question = e.target.dataset.question;
                this.elements.messageInput.value = question;
                this.sendMessage();
            });
        });
        
        // اقدامات سریع
        document.querySelectorAll('.quick-action').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.target.dataset.action;
                this.handleQuickAction(action);
            });
        });
        
        // تغییر تم
        document.getElementById('themeToggle').addEventListener('click', () => this.toggleTheme());
        
        // نمایش/مخفی کردن پنل کناری
        document.getElementById('toggleSidebar').addEventListener('click', () => {
            document.getElementById('sidebar').classList.toggle('active');
        });
        
        // بستن پنل دیباگ
        this.elements.closeDebug.addEventListener('click', () => {
            this.elements.debugPanel.classList.remove('show');
        });
        
        // کپی شناسه جلسه
        document.getElementById('sessionId').addEventListener('click', () => {
            this.copyToClipboard(this.sessionId);
            this.showToast('شناسه جلسه کپی شد!');
        });
    }
    
    async testConnection() {
        this.log('آزمایش اتصال به API...', 'info');
        this.updateConnectionStatus('testing', 'در حال آزمایش اتصال...');
        
        try {
            const response = await fetch('/api/health');
            if (response.ok) {
                const data = await response.json();
                this.log(`اتصال API موفق: ${data.status}`, 'success');
                this.updateConnectionStatus('connected', 'API فعال');
                return true;
            } else {
                this.log('پاسخ API ناموفق بود', 'warning');
                this.updateConnectionStatus('warning', 'API پاسخ نداد');
                return false;
            }
        } catch (error) {
            this.log(`خطا در اتصال به API: ${error.message}`, 'error');
            this.updateConnectionStatus('error', 'عدم اتصال به سرور');
            return false;
        }
    }
    
    updateConnectionStatus(status, message) {
        const alert = this.elements.connectionAlert;
        const statusDot = this.elements.sidebarStatus.querySelector('.status-dot');
        
        // پاک کردن کلاس‌های قبلی
        alert.className = 'connection-alert';
        statusDot.className = 'status-dot';
        
        switch(status) {
            case 'connected':
                alert.classList.add('connected');
                statusDot.style.background = '#10b981';
                this.elements.retryBtn.style.display = 'none';
                break;
            case 'testing':
                alert.classList.add('testing');
                statusDot.style.background = '#f59e0b';
                statusDot.style.animation = 'pulse 1s infinite';
                break;
            case 'warning':
                alert.classList.add('warning');
                statusDot.style.background = '#f59e0b';
                break;
            case 'error':
                alert.classList.add('error');
                statusDot.style.background = '#ef4444';
                this.elements.retryBtn.style.display = 'flex';
                break;
            case 'disconnected':
                statusDot.style.background = '#9ca3af';
                this.elements.retryBtn.style.display = 'flex';
                break;
        }
        
        this.elements.alertText.innerHTML = `<i class="fas fa-${this.getStatusIcon(status)}"></i> ${message}`;
        this.elements.sidebarStatus.innerHTML = `<span class="status-dot"></span> ${message}`;
    }
    
    getStatusIcon(status) {
        switch(status) {
            case 'connected': return 'wifi';
            case 'testing': return 'sync fa-spin';
            case 'warning': return 'exclamation-triangle';
            case 'error': return 'exclamation-circle';
            default: return 'plug';
        }
    }
    
    async sendMessage() {
        const message = this.elements.messageInput.value.trim();
        if (!message) return;
        
        // نمایش پیام کاربر
        this.addMessage(message, 'user');
        this.elements.messageInput.value = '';
        this.messageCount++;
        
        // ذخیره در localStorage
        this.saveConversation({ role: 'user', content: message });
        
        // نمایش نشانگر "در حال تایپ"
        this.showTypingIndicator();
        
        // اگر WebSocket وصل نیست، از REST API استفاده کن
        if (!this.isConnected) {
            this.log('ارسال از طریق REST API (WebSocket قطع است)', 'warning');
            await this.sendViaRestAPI(message);
        } else {
            // ارسال از طریق WebSocket
            this.sendViaWebSocket(message);
        }
    }
    
    async sendViaRestAPI(message) {
        try {
            const response = await fetch(`/api/chat/${this.sessionId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            this.hideTypingIndicator();
            this.addMessage(data.answer, 'bot', data.analysis);
            
            // به‌روزرسانی آمار
            this.updateStats();
            
        } catch (error) {
            this.hideTypingIndicator();
            this.log(`خطا در ارسال پیام: ${error.message}`, 'error');
            this.addMessage(
                'متأسفانه در حال حاضر امکان برقراری ارتباط با سرور وجود ندارد. لطفاً اتصال اینترنت خود را بررسی کنید یا دوباره تلاش کنید.',
                'system'
            );
        }
    }
    
    sendViaWebSocket(message) {
        if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
            this.log('WebSocket آماده نیست، استفاده از REST API', 'warning');
            this.sendViaRestAPI(message);
            return;
        }
        
        this.ws.send(JSON.stringify({
            type: 'message',
            content: message,
            session_id: this.sessionId,
            timestamp: new Date().toISOString()
        }));
    }
    
    handleQuickAction(action) {
        switch(action) {
            case 'test-api':
                this.testConnection();
                this.showToast('در حال آزمایش اتصال...');
                break;
            case 'clear-chat':
                if (confirm('آیا مطمئن هستید که می‌خواهید کل گفتگو را پاک کنید؟')) {
                    this.clearChat();
                    this.showToast('گفتگو پاک شد');
                }
                break;
            case 'export-chat':
                this.exportConversations();
                break;
            case 'view-logs':
                this.elements.debugPanel.classList.add('show');
                break;
        }
    }
    
    showToast(message, type = 'info') {
        // ایجاد یک toast موقت
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 100px;
            right: 20px;
            background: ${type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : '#3b82f6'};
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            z-index: 10000;
            animation: slideUp 0.3s ease-out;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideUp 0.3s ease-out reverse';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
    
    updateStats() {
        this.elements.statQuestions.textContent = this.messageCount;
        // این قسمت می‌تواند از localStorage یا سرور خوانده شود
        const topics = new Set(this.conversations
            .filter(c => c.role === 'bot' && c.analysis)
            .map(c => c.analysis.topic));
        this.elements.statTopics.textContent = topics.size;
        
        // ذخیره در localStorage
        localStorage.setItem('natiq_message_count', this.messageCount);
    }
    
    displaySessionId() {
        const shortId = this.sessionId.substring(0, 12) + '...';
        this.elements.sessionId.textContent = shortId;
        this.elements.sessionId.title = this.sessionId;
    }
    
    loadTheme() {
        const savedTheme = localStorage.getItem('natiq_theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
        
        // به‌روزرسانی آیکون
        const themeIcon = document.querySelector('#themeToggle i');
        themeIcon.className = savedTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
    
    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('natiq_theme', newTheme);
        
        // به‌روزرسانی آیکون
        const themeIcon = document.querySelector('#themeToggle i');
        themeIcon.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        
        this.log(`تم تغییر کرد به: ${newTheme === 'dark' ? 'تاریک' : 'روشن'}`, 'info');
    }
    
    // ... بقیه متدها (WebSocket، نمایش پیام، مدیریت مکالمات و غیره)
    // این بخش‌ها مشابه قبل هستند، اما با سیستم لاگ یکپارچه‌ شده‌اند
}

// راه‌اندازی برنامه
document.addEventListener('DOMContentLoaded', () => {
    window.natiqApp = new NatiqUltimateUI();
    
    // نمایش پنل دیباگ با دوبار کلیک روی لوگو
    document.querySelector('.logo').addEventListener('dblclick', () => {
        document.getElementById('debugPanel').classList.add('show');
    });
});
