// public/assets/js/chat.js
class NatiqChat {
    constructor() {
        this.apiBase = window.location.origin;
        this.sessionId = 'session_' + Date.now();
        this.conversation = [];
        this.init();
    }
    
    init() {
        this.loadSystemStatus();
        this.setupEventListeners();
    }
    
    async sendMessage() {
        const input = document.getElementById('messageInput');
        const message = input.value.trim();
        
        if (!message) return;
        
        // نمایش پیام کاربر
        this.addMessage(message, 'user');
        input.value = '';
        
        // نشانگر در حال پردازش
        this.showTypingIndicator();
        
        try {
            const response = await fetch(`${this.apiBase}/api/ask`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({question: message, session_id: this.sessionId})
            });
            
            const data = await response.json();
            this.hideTypingIndicator();
            
            if (data.success) {
                this.addMessage(data.response, 'bot');
                this.updateSystemStats();
            }
        } catch (error) {
            this.addMessage('خطا در ارتباط با سرور', 'bot');
        }
    }
    
    addMessage(text, sender) {
        // منطق اضافه کردن پیام به چت
    }
}
