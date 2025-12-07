// natiq-ultimate Frontend Application
class NatiqApp {
    constructor() {
        this.apiBase = window.location.origin;
        this.sessionId = 'session_' + Date.now();
        this.conversation = [];
        this.systemStatus = {
            neural: true,
            knowledge: true,
            api: true,
            integration: true
        };
        this.isDarkMode = false;
        
        this.init();
    }
    
    init() {
        console.log('🧠 natiq-ultimate v6.0 frontend initialized');
        
        // Initialize event listeners
        this.setupEventListeners();
        
        // Check system status on load
        this.checkSystemStatus();
        
        // Update UI with session info
        this.updateSessionInfo();
        
        // Handle character count
        this.setupCharacterCount();
        
        // Hide loading overlay after 1 second
        setTimeout(() => {
            this.hideLoading();
        }, 1000);
    }
    
    setupEventListeners() {
        // Send button click
        document.getElementById('sendButton').addEventListener('click', () => this.sendMessage());
        
        // Enter key in textarea
        document.getElementById('messageInput').addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Character count
        document.getElementById('messageInput').addEventListener('input', (e) => {
            this.updateCharacterCount(e.target.value.length);
        });
        
        // Quick question buttons
        document.querySelectorAll('.quick-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const question = e.target.textContent;
                document.getElementById('messageInput').value = question;
                this.sendMessage();
            });
        });
        
        // Test endpoint buttons
        document.querySelectorAll('.test-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const endpoint = e.target.getAttribute('onclick').match(/'([^']+)'/)[1];
                this.testEndpoint(endpoint);
            });
        });
        
        // Copy code buttons
        document.querySelectorAll('.copy-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const codeId = e.target.getAttribute('onclick').match(/'([^']+)'/)[1];
                this.copyCode(codeId);
            });
        });
    }
    
    setupCharacterCount() {
        const input = document.getElementById('messageInput');
        input.addEventListener('input', () => {
            const count = input.value.length;
            document.getElementById('charCount').textContent = count;
            
            if (count > 1000) {
                document.getElementById('charCount').style.color = '#ef4444';
            } else if (count > 800) {
                document.getElementById('charCount').style.color = '#f59e0b';
            } else {
                document.getElementById('charCount').style.color = '';
            }
        });
    }
    
    updateCharacterCount(count) {
        document.getElementById('charCount').textContent = count;
    }
    
    async sendMessage() {
        const input = document.getElementById('messageInput');
        const message = input.value.trim();
        
        if (!message) {
            this.showNotification('لطفاً یک سوال بنویسید', 'warning');
            return;
        }
        
        if (message.length > 1000) {
            this.showNotification('سوال نباید بیشتر از ۱۰۰۰ کاراکتر باشد', 'warning');
            return;
        }
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input
        input.value = '';
        this.updateCharacterCount(0);
        
        // Reset textarea height
        input.style.height = 'auto';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        // Disable send button
        const sendBtn = document.getElementById('sendButton');
        sendBtn.disabled = true;
        sendBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> در حال پردازش...';
        
        try {
            // Send request to backend
            const response = await fetch(`${this.apiBase}/api/ask`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: message,
                    session_id: this.sessionId,
                    timestamp: new Date().toISOString()
                })
            });
            
            const data = await response.json();
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            if (data.success) {
                // Add bot response
                this.addMessage(data.response, 'bot');
                
                // Update conversation history
                this.conversation.push({
                    question: message,
                    response: data.response,
                    timestamp: new Date().toISOString(),
                    analysis: data.analysis
                });
                
                // Update system info if available
                if (data.system) {
                    this.updateSystemInfo(data.system);
                }
                
                // Show analysis in notification
                if (data.analysis && data.analysis.confidence) {
                    this.showNotification(
                        `✅ پاسخ تولید شد (اطمینان: ${(data.analysis.confidence * 100).toFixed(1)}%)`,
                        'success'
                    );
                }
            } else {
                this.addMessage(`❌ خطا: ${data.error || 'پاسخ دریافت نشد'}`, 'bot');
                this.showNotification('خطا در دریافت پاسخ', 'error');
            }
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            
            let errorMessage = '';
            if (error.message.includes('Failed to fetch')) {
                errorMessage = '🔌 ارتباط با سرور برقرار نشد. لطفاً اتصال اینترنت را بررسی کنید.';
            } else {
                errorMessage = `⚠️ خطای پردازش: ${error.message}`;
            }
            
            this.addMessage(errorMessage, 'bot');
            this.showNotification('خطا در ارتباط با سرور', 'error');
        } finally {
            // Re-enable send button
            sendBtn.disabled = false;
            sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i> ارسال به سیستم';
            
            // Focus input
            input.focus();
        }
    }
    
    addMessage(content, sender) {
        const messagesContainer = document.getElementById('chatMessages');
        
        // Create message element
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        // Format time
        const time = new Date().toLocaleTimeString('fa-IR', {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        // Create avatar
        const avatar = sender === 'user' ? 
            '<i class="fas fa-user"></i>' : 
            '<i class="fas fa-brain"></i>';
        
        // Create message HTML
        messageDiv.innerHTML = `
            <div class="avatar">
                ${avatar}
            </div>
            <div class="message-content">
                <div class="message-header">
                    <span class="sender">${sender === 'user' ? 'شما' : 'سیستم عصبی-نمادین'}</span>
                    <span class="time">${time}</span>
                </div>
                <div class="message-body">
                    ${this.formatMessage(content)}
                </div>
            </div>
        `;
        
        // Add to chat
        messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Update conversation count
        this.updateConversationStats();
    }
    
    formatMessage(text) {
        // Convert markdown-like formatting
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>')
            .replace(/✅/g, '<span class="emoji success">✅</span>')
            .replace(/⚠️/g, '<span class="emoji warning">⚠️</span>')
            .replace(/❌/g, '<span class="emoji error">❌</span>')
            .replace(/🔍/g, '<span class="emoji info">🔍</span>')
            .replace(/🎯/g, '<span class="emoji">🎯</span>')
            .replace(/📚/g, '<span class="emoji">📚</span>')
            .replace(/🧠/g, '<span class="emoji">🧠</span>');
    }
    
    showTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        indicator.style.display = 'flex';
        
        // Scroll to bottom
        const messagesContainer = document.getElementById('chatMessages');
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    hideTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        indicator.style.display = 'none';
    }
    
    async checkSystemStatus() {
        try {
            const response = await fetch(`${this.apiBase}/api/health`);
            const data = await response.json();
            
            // Update status indicators
            this.updateStatusIndicators(data);
            
            // Update last update time
            document.getElementById('lastUpdate').textContent = 
                `آخرین بروزرسانی: ${new Date().toLocaleTimeString('fa-IR')}`;
            
            // Update uptime
            if (data.statistics) {
                this.updateUptime(data.statistics);
            }
            
        } catch (error) {
            console.error('Error checking system status:', error);
            this.showNotification('خطا در بررسی وضعیت سیستم', 'error');
        }
    }
    
    updateStatusIndicators(data) {
        // Update system status based on health check
        const statusItems = document.querySelectorAll('.status-item');
        
        if (data.components) {
            const statusMap = {
                'سیستم عصبی': data.components.neural_system,
                'پایگاه دانش': data.components.knowledge_graph,
                'API Gateway': data.components.api_gateway,
                'یکپارچه‌سازی': 'operational' // Assuming integration is operational
            };
            
            statusItems.forEach(item => {
                const title = item.querySelector('h4').textContent;
                const status = statusMap[title];
                const indicator = item.querySelector('.status-indicator');
                
                if (status === 'operational') {
                    indicator.innerHTML = '<span>فعال</span>';
                    indicator.style.background = 'rgba(16, 185, 129, 0.1)';
                    indicator.style.color = '#10b981';
                    indicator.querySelector('span').before(this.createStatusDot('#10b981'));
                } else {
                    indicator.innerHTML = '<span>مشکل</span>';
                    indicator.style.background = 'rgba(239, 68, 68, 0.1)';
                    indicator.style.color = '#ef4444';
                    indicator.querySelector('span').before(this.createStatusDot('#ef4444'));
                }
            });
        }
    }
    
    createStatusDot(color) {
        const dot = document.createElement('span');
        dot.style.cssText = `
            width: 6px;
            height: 6px;
            background: ${color};
            border-radius: 50%;
            display: inline-block;
            margin-left: 4px;
        `;
        return dot;
    }
    
    updateUptime(stats) {
        // This is a simplified uptime calculation
        // In a real system, you would get this from the backend
        const uptimeElement = document.getElementById('uptime');
        uptimeElement.textContent = '۱۰۰٪';
    }
    
    updateSystemInfo(systemInfo) {
        // Update system info in UI if needed
        console.log('System info updated:', systemInfo);
    }
    
    updateSessionInfo() {
        // Update session ID in UI
        const sessionElement = document.querySelector('#sessionId');
        if (sessionElement) {
            sessionElement.textContent = this.sessionId.substring(0, 10) + '...';
        }
    }
    
    updateConversationStats() {
        // Update conversation stats
        const count = this.conversation.length;
        // You could update stats in the header or dashboard
    }
    
    async testEndpoint(endpoint) {
        this.showLoading();
        
        try {
            const response = await fetch(`${this.apiBase}${endpoint}`);
            const data = await response.json();
            
            this.showNotification(
                `✅ ${endpoint} پاسخ داد با کد ${response.status}`,
                'success'
            );
            
            console.log(`Test ${endpoint}:`, data);
            
        } catch (error) {
            this.showNotification(
                `❌ خطا در تست ${endpoint}: ${error.message}`,
                'error'
            );
            console.error(`Test ${endpoint} error:`, error);
        } finally {
            this.hideLoading();
        }
    }
    
    copyCode(elementId) {
        const element = document.getElementById(elementId);
        const code = element.textContent;
        
        navigator.clipboard.writeText(code).then(() => {
            this.showNotification('✅ کد کپی شد', 'success');
        }).catch(err => {
            console.error('Failed to copy:', err);
            this.showNotification('❌ خطا در کپی کردن', 'error');
        });
    }
    
    clearChat() {
        if (confirm('آیا مطمئن هستید که می‌خواهید همه مکالمه را پاک کنید؟')) {
            const messagesContainer = document.getElementById('chatMessages');
            
            // Keep only the first message (welcome message)
            while (messagesContainer.children.length > 1) {
                messagesContainer.removeChild(messagesContainer.lastChild);
            }
            
            // Clear conversation array
            this.conversation = [];
            
            this.showNotification('✅ مکالمه پاک شد', 'success');
        }
    }
    
    exportChat() {
        const chatData = {
            session_id: this.sessionId,
            timestamp: new Date().toISOString(),
            conversation: this.conversation
        };
        
        const dataStr = JSON.stringify(chatData, null, 2);
        const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
        
        const exportFileDefaultName = `natiq-chat-${this.sessionId}.json`;
        
        const linkElement = document.createElement('a');
        linkElement.setAttribute('href', dataUri);
        linkElement.setAttribute('download', exportFileDefaultName);
        linkElement.click();
        
        this.showNotification('✅ مکالمه ذخیره شد', 'success');
    }
    
    toggleDarkMode() {
        this.isDarkMode = !this.isDarkMode;
        document.body.classList.toggle('dark-mode', this.isDarkMode);
        
        const icon = document.querySelector('.icon-btn .fa-moon');
        if (this.isDarkMode) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
            this.showNotification('تم تیره فعال شد', 'success');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
            this.showNotification('تم روشن فعال شد', 'success');
        }
    }
    
    showLoading() {
        document.getElementById('loadingOverlay').style.display = 'flex';
    }
    
    hideLoading() {
        document.getElementById('loadingOverlay').style.display = 'none';
    }
    
    showNotification(message, type = 'info') {
        const notification = document.getElementById('notification');
        
        // Set message and type
        notification.textContent = message;
        notification.className = `notification ${type}`;
        
        // Show notification
        notification.style.display = 'flex';
        
        // Auto hide after 3 seconds
        setTimeout(() => {
            notification.style.display = 'none';
        }, 3000);
    }
    
    scrollToChat() {
        document.getElementById('chat').scrollIntoView({
            behavior: 'smooth'
        });
    }
    
    showAbout() {
        alert('natiq-ultimate v6.0\nسیستم هوش مصنوعی عصبی-نمادین\n\nنسخه: 6.0.0\nتاریخ انتشار: ۱۴۰۲/۰۹/۱۷\n\nتمامی حقوق محفوظ است.');
    }
    
    showTerms() {
        alert('شرایط استفاده از سیستم:\n\n1. این سیستم برای استفاده آموزشی و تحقیقاتی ارائه شده است.\n2. پاسخ‌ها بر اساس دانش موجود تولید می‌شوند.\n3. مسئولیت استفاده از اطلاعات بر عهده کاربر است.');
    }
}

// Global functions for HTML onclick handlers
function scrollToChat() {
    window.chatApp.scrollToChat();
}

function clearChat() {
    window.chatApp.clearChat();
}

function exportChat() {
    window.chatApp.exportChat();
}

function toggleDarkMode() {
    window.chatApp.toggleDarkMode();
}

function testEndpoint(endpoint) {
    window.chatApp.testEndpoint(endpoint);
}

function copyCode(elementId) {
    window.chatApp.copyCode(elementId);
}

function askQuestion(question) {
    document.getElementById('messageInput').value = question;
    window.chatApp.sendMessage();
}

function showAbout() {
    window.chatApp.showAbout();
}

function showTerms() {
    window.chatApp.showTerms();
}

function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        window.chatApp.sendMessage();
    }
}

// Initialize app when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.chatApp = new NatiqApp();
});

