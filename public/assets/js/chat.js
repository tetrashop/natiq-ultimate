class NatiqChat {
    constructor() {
        this.apiBase = window.location.origin;  // تغییر به پورت 8081
        this.sessionId = 'session_' + Date.now();
        this.conversation = [];
        this.messageCount = 0;
        this.isProcessing = false;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.updateSessionId();
    }
    
    setupEventListeners() {
        const textarea = document.getElementById('messageInput');
        
        if (textarea) {
            textarea.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
            
            textarea.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = Math.min(this.scrollHeight, 150) + 'px';
            });
        }
        
        document.querySelectorAll('.quick-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                if (this.isProcessing) return;
                const question = e.target.textContent.trim();
                const input = document.getElementById('messageInput');
                if (input) {
                    input.value = question;
                    this.sendMessage();
                }
            });
        });
    }
    
    updateSessionId() {
        const sessionElement = document.getElementById('sessionId');
        if (sessionElement) {
            sessionElement.textContent = this.sessionId;
        }
    }
    
    async sendMessage() {
        if (this.isProcessing) {
            this.showToast('لطفاً صبر کنید تا پاسخ قبلی دریافت شود', 'info');
            return;
        }
        
        const input = document.getElementById('messageInput');
        const message = input ? input.value.trim() : '';
        
        if (!message) {
            this.showToast('لطفاً پیامی وارد کنید', 'warning');
            if (input) input.focus();
            return;
        }
        
        this.addMessage(message, 'user');
        if (input) {
            input.value = '';
            input.style.height = 'auto';
        }
        
        this.showTypingIndicator();
        this.isProcessing = true;
        
        try {
            const response = await fetch(`window.location.origin + '/api/ask'`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    question: message,
                    session_id: this.sessionId,
                    timestamp: new Date().toISOString()
                })
            });
            
            const data = await response.json();
            this.hideTypingIndicator();
            
            if (data.success) {
                this.addMessage(data.response, 'bot');
                this.updateStats();
            } else {
                this.addMessage('متأسفانه در پردازش سوال شما خطایی رخ داد.', 'bot');
            }
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage('سیستم در حالت آفلاین کار می‌کند. پاسخ نمونه:', 'bot');
            this.addMessage(`شما پرسیدید: "${message}". این یک پاسخ آفلاین از natiq-ultimate است.`, 'bot');
        } finally {
            this.isProcessing = false;
        }
    }
    
    addMessage(text, sender) {
        const messagesContainer = document.getElementById('chatMessages');
        if (!messagesContainer) return;
        
        const messageElement = document.createElement('div');
        messageElement.className = `message ${sender}`;
        
        const now = new Date();
        const timeString = now.toLocaleTimeString('fa-IR', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        
        messageElement.innerHTML = `
            <div class="message-header">
                <i class="fas fa-${sender === 'user' ? 'user' : 'robot'}"></i>
                <span>${sender === 'user' ? 'شما' : 'دستیار هوشمند'}</span>
                <span class="message-time">${timeString}</span>
            </div>
            <div class="message-content">${this.formatMessage(text)}</div>
        `;
        
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    formatMessage(text) {
        let formatted = text
            .replace(/\n/g, '<br>')
            .replace(/```([\s\S]*?)```/g, '<div class="code-block">$1</div>')
            .replace(/`([^`]+)`/g, '<code>$1</code>');
        
        return formatted;
    }
    
    showTypingIndicator() {
        const messagesContainer = document.getElementById('chatMessages');
        if (!messagesContainer) return;
        
        const typingElement = document.createElement('div');
        typingElement.id = 'typingIndicator';
        typingElement.className = 'typing-indicator';
        typingElement.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <span>در حال پردازش...</span>
        `;
        
        messagesContainer.appendChild(typingElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    hideTypingIndicator() {
        const typingElement = document.getElementById('typingIndicator');
        if (typingElement) {
            typingElement.remove();
        }
    }
    
    updateStats() {
        const todayRequests = document.getElementById('todayRequests');
        if (todayRequests) {
            let count = parseInt(todayRequests.textContent) || 0;
            todayRequests.textContent = count + 1;
        }
    }
    
    showToast(message, type = 'info') {
        // پیاده‌سازی ساده توستر
        alert(`[${type}] ${message}`);
    }
    
    askQuestion(question) {
        if (this.isProcessing) return;
        
        const input = document.getElementById('messageInput');
        if (input) {
            input.value = question;
            this.sendMessage();
        }
    }
}

// ایجاد نمونه از کلاس چت
window.chat = new NatiqChat();

// توابع سراسری
window.sendMessage = () => window.chat.sendMessage();
window.askQuestion = (question) => window.chat.askQuestion(question);
window.clearChat = () => {
    if (confirm('آیا مطمئن هستید که می‌خواهید تاریخچه چت را پاک کنید؟')) {
        const messagesContainer = document.getElementById('chatMessages');
        if (messagesContainer) {
            messagesContainer.innerHTML = '';
        }
    }
};
