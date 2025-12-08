class NatiqChat {
    constructor() {
        this.apiBase = window.location.origin;
        this.conversation = [];
    }
    
    async sendMessage() {
        const input = document.getElementById('messageInput');
        const message = input.value.trim();
        
        if (!message) return;
        
        // نمایش پیام کاربر
        this.addMessage(message, 'user');
        input.value = '';
        
        try {
            const response = await fetch(this.apiBase + '/api/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({question: message})
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.addMessage(data.response, 'bot');
            } else {
                this.addMessage('پاسخ دریافت نشد', 'bot');
            }
        } catch (error) {
            this.addMessage('سیستم در حالت آفلاین کار می‌کند', 'bot');
        }
    }
    
    addMessage(text, sender) {
        const messagesContainer = document.getElementById('chatMessages');
        if (!messagesContainer) return;
        
        const messageElement = document.createElement('div');
        messageElement.className = `message ${sender}`;
        messageElement.innerHTML = `
            <div class="message-content">${text}</div>
        `;
        
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

// ایجاد نمونه
const chat = new NatiqChat();
window.sendMessage = () => chat.sendMessage();
