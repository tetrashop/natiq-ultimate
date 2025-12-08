class NatiqChat {
    constructor() {
        this.apiBase = window.location.origin;
        this.sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        this.conversation = [];
        this.messageCount = 0;
        this.isProcessing = false;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.updateSessionId();
        this.loadConversation();
    }
    
    setupEventListeners() {
        const textarea = document.getElementById('messageInput');
        
        // Enter برای ارسال، Shift+Enter برای خط جدید
        textarea.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-resize textarea
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 150) + 'px';
        });
        
        // دکمه‌های سریع
        document.querySelectorAll('.quick-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                if (this.isProcessing) return;
                const question = e.target.textContent.trim();
                document.getElementById('messageInput').value = question;
                this.sendMessage();
            });
        });
    }
    
    updateSessionId() {
        document.getElementById('sessionId').textContent = this.sessionId;
    }
    
    async sendMessage() {
        if (this.isProcessing) {
            showToast('لطفاً صبر کنید تا پاسخ قبلی دریافت شود', 'info');
            return;
        }
        
        const input = document.getElementById('messageInput');
        const message = input.value.trim();
        
        if (!message) {
            showToast('لطفاً پیامی وارد کنید', 'warning');
            input.focus();
            return;
        }
        
        // نمایش پیام کاربر
        this.addMessage(message, 'user');
        input.value = '';
        input.style.height = 'auto';
        
        // نشانگر تایپینگ
        this.showTypingIndicator();
        
        this.isProcessing = true;
        
        try {
            const startTime = Date.now();
            
            const response = await fetch(`${this.apiBase}/api/ask`, {
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
            
            const processingTime = Date.now() - startTime;
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            this.hideTypingIndicator();
            
            if (data.success) {
                // نمایش پاسخ AI
                this.addMessage(data.response, 'bot');
                
                // به‌روزرسانی آمار
                this.updateStats();
                
                // نمایش زمان پردازش
                this.showProcessingTime(processingTime);
                
                // ذخیره مکالمه
                this.saveConversation();
            } else {
                this.addMessage('متأسفانه در پردازش سوال شما خطایی رخ داد. لطفاً دوباره تلاش کنید.', 'bot');
                console.error('API Error:', data.error);
            }
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage('خطا در ارتباط با سرور. لطفاً اتصال اینترنت خود را بررسی کنید و دوباره تلاش نمایید.', 'bot');
            console.error('Network Error:', error);
            showToast('خطا در ارتباط با سرور', 'error');
        } finally {
            this.isProcessing = false;
        }
    }
    
    addMessage(text, sender) {
        const messagesContainer = document.getElementById('chatMessages');
        
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
        
        // ذخیره در تاریخچه
        this.conversation.push({
            sender,
            text,
            timestamp: now.toISOString(),
            messageId: `msg_${Date.now()}_${this.messageCount++}`
        });
    }
    
    formatMessage(text) {
        // تبدیل لینک‌ها به تگ <a>
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        let formatted = text.replace(urlRegex, url => 
            `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`
        );
        
        // فرمت کد
        const codeRegex = /```([\s\S]*?)```/g;
        formatted = formatted.replace(codeRegex, (match, code) => 
            `<div class="code-block">${escapeHtml(code.trim())}</div>`
        );
        
        // فرمت inline code
        const inlineCodeRegex = /`([^`]+)`/g;
        formatted = formatted.replace(inlineCodeRegex, (match, code) => 
            `<code>${escapeHtml(code)}</code>`
        );
        
        // تبدیل خطوط جدید به <br>
        formatted = formatted.replace(/\n/g, '<br>');
        
        return formatted;
    }
    
    showTypingIndicator() {
        const messagesContainer = document.getElementById('chatMessages');
        
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
        let count = parseInt(todayRequests.textContent) || 0;
        todayRequests.textContent = count + 1;
        
        // ذخیره در localStorage
        const today = new Date().toDateString();
        const stats = JSON.parse(localStorage.getItem('natiq_stats') || '{}');
        
        if (stats.date !== today) {
            stats.date = today;
            stats.count = 1;
        } else {
            stats.count = (stats.count || 0) + 1;
        }
        
        localStorage.setItem('natiq_stats', JSON.stringify(stats));
    }
    
    showProcessingTime(time) {
        // نمایش زمان پردازش به صورت ظریف
        if (time > 3000) {
            showToast(`پاسخ در ${(time/1000).toFixed(1)} ثانیه آماده شد`, 'info', 2000);
        }
    }
    
    saveConversation() {
        try {
            const conversationData = {
                sessionId: this.sessionId,
                messages: this.conversation,
                lastUpdated: new Date().toISOString()
            };
            
            localStorage.setItem(`natiq_conversation_${this.sessionId}`, JSON.stringify(conversationData));
            
            // ذخیره خلاصه مکالمه‌ها
            const allSessions = JSON.parse(localStorage.getItem('natiq_sessions') || '[]');
            if (!allSessions.includes(this.sessionId)) {
                allSessions.push(this.sessionId);
                localStorage.setItem('natiq_sessions', JSON.stringify(allSessions.slice(-10))); // فقط 10 جلسه آخر
            }
        } catch (error) {
            console.error('خطا در ذخیره مکالمه:', error);
        }
    }
    
    loadConversation() {
        try {
            const saved = localStorage.getItem(`natiq_conversation_${this.sessionId}`);
            if (saved) {
                const data = JSON.parse(saved);
                this.conversation = data.messages || [];
                
                // نمایش تاریخچه (اختیاری)
                // this.displayConversationHistory();
            }
        } catch (error) {
            console.error('خطا در بارگذاری مکالمه:', error);
        }
    }
    
    clearChat() {
        if (confirm('آیا مطمئن هستید که می‌خواهید تاریخچه چت را پاک کنید؟')) {
            const messagesContainer = document.getElementById('chatMessages');
            
            // حفظ اولین پیام خوشامد
            const welcomeMessage = messagesContainer.querySelector('.message.bot');
            messagesContainer.innerHTML = '';
            
            if (welcomeMessage) {
                messagesContainer.appendChild(welcomeMessage);
            }
            
            // پاک کردن تاریخچه حافظه
            this.conversation = [];
            localStorage.removeItem(`natiq_conversation_${this.sessionId}`);
            
            showToast('تاریخچه چت پاک شد', 'success');
        }
    }
    
    copySessionId() {
        copyToClipboard(this.sessionId);
    }
    
    exportConversation() {
        const exportData = {
            sessionId: this.sessionId,
            exportDate: new Date().toISOString(),
            messages: this.conversation,
            systemInfo: {
                version: 'natiq-ultimate v6.0',
                url: window.location.href
            }
        };
        
        const dataStr = JSON.stringify(exportData, null, 2);
        const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
        
        const exportFileDefaultName = `natiq-conversation-${this.sessionId}.json`;
        
        const linkElement = document.createElement('a');
        linkElement.setAttribute('href', dataUri);
        linkElement.setAttribute('download', exportFileDefaultName);
        linkElement.click();
        
        showToast('مکالمه با موفقیت ذخیره شد', 'success');
    }
    
    askQuestion(question) {
        if (this.isProcessing) return;
        
        document.getElementById('messageInput').value = question;
        this.sendMessage();
    }
}

// ایجاد یک نمونه از کلاس چت
const chat = new NatiqChat();

// توابع سراسری برای دسترسی از HTML
window.sendMessage = () => chat.sendMessage();
window.askQuestion = (question) => chat.askQuestion(question);
window.clearChat = () => chat.clearChat();
window.copySessionId = () => chat.copySessionId();
window.exportConversation = () => chat.exportConversation();
