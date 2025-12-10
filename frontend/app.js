// متغیرهای اصلی
const API_BASE_URL = window.location.origin;
let currentUser = {
    id: localStorage.getItem('user_id') || 'user_' + Math.random().toString(36).substr(2, 9),
    name: 'کاربر ریاضی',
    level: 'intermediate',
    preferences: JSON.parse(localStorage.getItem('user_prefs')) || {}
};

// مقداردهی اولیه برنامه
document.addEventListener('DOMContentLoaded', function() {
    initApp();
    loadUserData();
    setupEventListeners();
    checkSystemStatus();
    
    // نمایش نوتیفیکیشن خوش‌آمدگویی
    showNotification('به ناطق اولتیمیت خوش آمدید! 🎉', 'success');
});

// تابع مقداردهی اولیه برنامه
function initApp() {
    // تنظیم رویدادهای ناوبری
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const pageId = this.getAttribute('data-page');
            showPage(pageId);
            
            // به‌روزرسایی وضعیت فعال
            document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // تنظیم رویدادهای دکمه‌های سریع
    document.querySelectorAll('.action-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.getAttribute('data-action');
            handleQuickAction(action);
        });
    });
}

// تابع نمایش صفحات
function showPage(pageId) {
    // مخفی کردن همه صفحات
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // نمایش صفحه مورد نظر
    const targetPage = document.getElementById(pageId);
    if (targetPage) {
        targetPage.classList.add('active');
        
        // بارگذاری محتوای صفحه
        loadPageContent(pageId);
        
        // به‌روزرسانی تاریخچه
        addToPageHistory(pageId);
    }
}

// تابع بارگذاری محتوای صفحه
async function loadPageContent(pageId) {
    switch(pageId) {
        case 'math-solver':
            await loadMathSolver();
            break;
        case 'chat':
            await loadChatInterface();
            break;
        case 'dashboard':
            await loadDashboardData();
            break;
        case 'tutor':
            await loadTutorSystem();
            break;
    }
}

// تابع مدیریت اکشن‌های سریع
function handleQuickAction(action) {
    switch(action) {
        case 'solve-equation':
            showPage('math-solver');
            break;
        case 'chat':
            showPage('chat');
            break;
        case 'learn':
            showPage('tutor');
            break;
        case 'practice':
            generatePracticeProblem();
            break;
    }
}

// ==================== سیستم حل معادلات ====================
async function loadMathSolver() {
    // تنظیم رویدادهای حل‌کننده
    const solveBtn = document.getElementById('solve-btn');
    const equationInput = document.getElementById('equation-input');
    
    if (solveBtn) {
        solveBtn.addEventListener('click', async () => {
            const equation = equationInput.value.trim();
            if (!equation) {
                showNotification('لطفاً معادله‌ای وارد کنید', 'warning');
                return;
            }
            
            await solveEquation(equation);
        });
    }
    
    // تنظیم رویدادهای دکمه‌های نماد ریاضی
    document.querySelectorAll('.math-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const symbol = this.getAttribute('data-symbol');
            insertAtCursor(equationInput, symbol);
        });
    });
}

// تابع حل معادله
async function solveEquation(equation) {
    const loadingId = showLoading('در حال حل معادله...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/math/solve`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                equation: equation,
                variable: 'x'
            })
        });
        
        const data = await response.json();
        
        if (data.success && data.result) {
            displaySolution(data.result);
            saveToHistory('equation_solve', {
                equation: equation,
                solution: data.result.solutions,
                timestamp: new Date().toISOString()
            });
        } else {
            throw new Error(data.error || 'خطا در حل معادله');
        }
    } catch (error) {
        showNotification(`خطا: ${error.message}`, 'error');
    } finally {
        hideLoading(loadingId);
    }
}

// نمایش جواب
function displaySolution(result) {
    const solutionsOutput = document.getElementById('solutions-output');
    const stepsOutput = document.getElementById('steps-output');
    
    if (solutionsOutput) {
        solutionsOutput.innerHTML = `
            <div class="solution-item">
                <div class="solution-type">${result.type || 'معادله جبری'}</div>
                <div class="solution-equation">${result.equation}</div>
                <div class="solution-answers">
                    <strong>جواب‌ها:</strong>
                    ${result.solutions.map((sol, i) => `
                        <div class="answer">
                            <span class="answer-index">x${i+1} =</span>
                            <span class="answer-value">${sol}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    if (stepsOutput && result.steps) {
        stepsOutput.innerHTML = `
            <div class="steps-list">
                ${result.steps.map((step, i) => `
                    <div class="step">
                        <span class="step-number">مرحله ${i+1}:</span>
                        <span class="step-content">${step}</span>
                    </div>
                `).join('')}
            </div>
        `;
    }
}

// ==================== سیستم چت هوشمند ====================
async function loadChatInterface() {
    const sendBtn = document.getElementById('send-chat');
    const chatInput = document.getElementById('chat-input');
    
    if (sendBtn && chatInput) {
        // ارسال با کلیک
        sendBtn.addEventListener('click', sendChatMessage);
        
        // ارسال با Enter
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendChatMessage();
            }
        });
    }
    
    // بارگذاری sessionهای قبلی
    loadChatSessions();
    
    // تنظیم رویداد برای سوالات سریع
    document.querySelectorAll('.quick-question').forEach(btn => {
        btn.addEventListener('click', function() {
            const question = this.getAttribute('data-question');
            chatInput.value = question;
            sendChatMessage();
        });
    });
}

// تابع ارسال پیام چت
async function sendChatMessage() {
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();
    const chatMode = document.getElementById('chat-mode').value;
    
    if (!message) return;
    
    // نمایش پیام کاربر
    addChatMessage('user', message);
    chatInput.value = '';
    
    // ارسال به API
    try {
        const response = await fetch(`${API_BASE_URL}/api/chat-memory`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                session_id: currentUser.id + '_' + chatMode,
                context: {
                    mode: chatMode,
                    user_level: currentUser.level
                }
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            addChatMessage('bot', data.response);
            
            // تحلیل پاسخ برای ارائه پیشنهادات
            analyzeChatResponse(data.response);
        }
    } catch (error) {
        addChatMessage('error', 'خطا در ارتباط با سرور');
    }
}

// افزودن پیام به چت
function addChatMessage(sender, content) {
    const chatMessages = document.getElementById('chat-messages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const avatar = sender === 'user' ? 
        `<div class="user-avatar">
            <i class="fas fa-user"></i>
        </div>` :
        `<div class="bot-avatar">
            <i class="fas fa-robot"></i>
        </div>`;
    
    messageDiv.innerHTML = `
        ${sender === 'bot' ? avatar : ''}
        <div class="message-content">
            <div class="message-text">${content}</div>
            <div class="message-time">${new Date().toLocaleTimeString('fa-IR')}</div>
        </div>
        ${sender === 'user' ? avatar : ''}
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// ==================== سیستم داشبورد ====================
async function loadDashboardData() {
    // بارگذاری آمار کاربر
    await loadUserStats();
    
    // بارگذاری پیشنهادات هوشمند
    await loadAISuggestions();
    
    // بارگذاری فعالیت‌های اخیر
    loadRecentActivities();
}

// بارگذاری آمار کاربر
async function loadUserStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/user/stats`, {
            headers: {
                'User-ID': currentUser.id
            }
        });
        
        if (response.ok) {
            const stats = await response.json();
            updateStatsDisplay(stats);
        }
    } catch (error) {
        console.error('خطا در بارگذاری آمار:', error);
    }
}

// ==================== ابزارهای کمکی ====================
// نمایش نوتیفیکیشن
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 
                          type === 'error' ? 'exclamation-circle' : 
                          type === 'warning' ? 'exclamation-triangle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    // نمایش و حذف خودکار
    setTimeout(() => {
        notification.classList.add('show');
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }, 100);
}

// نمایش وضعیت لودینگ
function showLoading(message) {
    const loadingId = 'loading-' + Date.now();
    const loadingDiv = document.createElement('div');
    loadingDiv.id = loadingId;
    loadingDiv.className = 'loading-overlay';
    loadingDiv.innerHTML = `
        <div class="loading-content">
            <div class="spinner"></div>
            <p>${message}</p>
        </div>
    `;
    
    document.body.appendChild(loadingDiv);
    return loadingId;
}

function hideLoading(id) {
    const loading = document.getElementById(id);
    if (loading) {
        loading.classList.add('fade-out');
        setTimeout(() => {
            if (loading.parentNode) {
                loading.parentNode.removeChild(loading);
            }
        }, 300);
    }
}

// بررسی وضعیت سیستم
async function checkSystemStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        if (response.ok) {
            const data = await response.json();
            updateSystemStatus(data);
            
            // بروزرسانی خودکار هر 30 ثانیه
            setTimeout(checkSystemStatus, 30000);
        }
    } catch (error) {
        console.error('خطا در بررسی وضعیت سیستم:', error);
        setTimeout(checkSystemStatus, 10000);
    }
}

// ذخیره در تاریخچه
function saveToHistory(type, data) {
    let history = JSON.parse(localStorage.getItem('user_history') || '[]');
    history.unshift({
        type: type,
        data: data,
        timestamp: new Date().toISOString()
    });
    
    // نگه‌داری فقط 100 آیتم آخر
    history = history.slice(0, 100);
    localStorage.setItem('user_history', JSON.stringify(history));
}

// ==================== متدهای ریاضی کمکی ====================
// درج در مکان کursor
function insertAtCursor(textarea, text) {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const value = textarea.value;
    
    textarea.value = value.substring(0, start) + text + value.substring(end);
    textarea.selectionStart = textarea.selectionEnd = start + text.length;
    textarea.focus();
}

// تحلیل پاسخ چت برای ارائه پیشنهادات
function analyzeChatResponse(response) {
    const keywords = {
        'مشتق': ['حسابان', 'مشتق‌گیری'],
        'انتگرال': ['حسابان', 'انتگرال'],
        'معادله': ['جبر', 'حل معادله'],
        'هندسه': ['هندسه', 'اشکال'],
        'احتمال': ['آمار', 'احتمال']
    };
    
    for (const [keyword, topics] of Object.entries(keywords)) {
        if (response.includes(keyword)) {
            setTimeout(() => {
                showNotification(
                    `پیشنهاد: می‌خواهید بیشتر درباره ${topics[0]} یاد بگیرید؟`,
                    'info'
                );
            }, 1000);
            break;
        }
    }
}

// بارگذاری پیشنهادات هوشمند
async function loadAISuggestions() {
    // اینجا می‌توانیم از API هوش مصنوعی استفاده کنیم
    const suggestions = [
        {
            title: "تمرین معادلات درجه دوم",
            description: "بر اساس فعالیت‌های اخیر شما پیشنهاد می‌شود",
            icon: "fas fa-square-root-alt",
            action: "practice_quadratic"
        },
        {
            title: "مباحث پیشرفته حسابان",
            description: "آماده چالش جدید هستید؟",
            icon: "fas fa-infinity",
            action: "learn_calculus"
        }
    ];
    
    const container = document.querySelector('.ai-suggestions');
    if (container) {
        container.innerHTML = suggestions.map(s => `
            <div class="suggestion" data-action="${s.action}">
                <i class="${s.icon}"></i>
                <div class="suggestion-content">
                    <h4>${s.title}</h4>
                    <p>${s.description}</p>
                </div>
                <button class="btn-sm">شروع</button>
            </div>
        `).join('');
    }
}

// اجرای برنامه
initApp();

