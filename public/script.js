// متغیرهای اصلی
const API_BASE_URL = window.location.origin;
let serverData = null;

// مقداردهی اولیه
document.addEventListener('DOMContentLoaded', async () => {
    // بررسی وضعیت سرور
    await checkServerStatus();
    
    // بارگذاری endpointها
    loadEndpoints();
    
    // تنظیم event listeners
    setupEventListeners();
    
    // به‌روزرسانی آدرس API
    document.getElementById('apiUrl').textContent = API_BASE_URL;
});

// بررسی وضعیت سرور
async function checkServerStatus() {
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.getElementById('serverStatus');
    const statusBadge = document.getElementById('statusBadge');
    
    try {
        const startTime = Date.now();
        const response = await fetch(`${API_BASE_URL}/api/health`);
        const endTime = Date.now();
        
        if (response.ok) {
            const data = await response.json();
            serverData = data;
            
            // به‌روزرسانی UI
            statusDot.classList.add('online');
            statusText.textContent = 'فعال';
            statusText.classList.add('running');
            statusBadge.innerHTML = `
                <span class="status-dot online"></span>
                <span>فعال (${endTime - startTime}ms)</span>
            `;
            
            // به‌روزرسانی نسخه
            if (data.version) {
                document.getElementById('version').textContent = data.version;
            }
            
            showNotification('✅ سرور فعال و آماده است', 'success');
        } else {
            throw new Error('پاسخ غیر موفق');
        }
    } catch (error) {
        console.error('خطا در بررسی وضعیت:', error);
        
        // به‌روزرسانی UI برای حالت خطا
        statusText.textContent = 'غیرفعال';
        statusText.classList.remove('running');
        statusText.classList.add('error');
        statusBadge.innerHTML = `
            <span class="status-dot" style="background: #f72585"></span>
            <span>خطا در اتصال</span>
        `;
        
        showNotification('⚠️ خطا در اتصال به سرور', 'error');
    }
}

// بارگذاری endpointها
function loadEndpoints() {
    const endpointList = document.getElementById('endpointList');
    const endpoints = [
        {
            method: 'GET',
            path: '/api/health',
            description: 'بررسی وضعیت سلامت سرور و دریافت اطلاعات نسخه'
        },
        {
            method: 'POST',
            path: '/api/chat',
            description: 'چت ساده بدون ذخیره حافظه - برای درخواست‌های مستقل'
        },
        {
            method: 'POST',
            path: '/api/chat-memory',
            description: 'چت هوشمند با قابلیت ذخیره حافظه مکالمه - نیاز به session_id'
        }
    ];
    
    endpointList.innerHTML = endpoints.map(endpoint => `
        <div class="endpoint-item">
            <div>
                <span class="endpoint-method method-${endpoint.method.toLowerCase()}">
                    ${endpoint.method}
                </span>
                <span class="endpoint-path">${endpoint.path}</span>
            </div>
            <div class="endpoint-desc">${endpoint.description}</div>
        </div>
    `).join('');
}

// تنظیم event listeners
function setupEventListeners() {
    const endpointSelect = document.getElementById('endpointSelect');
    const messageGroup = document.getElementById('messageGroup');
    const sessionGroup = document.getElementById('sessionGroup');
    
    // تغییر endpoint در select
    endpointSelect.addEventListener('change', function() {
        const isChatEndpoint = this.value.includes('/api/chat');
        messageGroup.style.display = isChatEndpoint ? 'flex' : 'none';
        sessionGroup.style.display = this.value === '/api/chat-memory' ? 'flex' : 'none';
    });
}

// تست endpoint انتخابی
async function testEndpoint() {
    const endpointSelect = document.getElementById('endpointSelect');
    const messageInput = document.getElementById('messageInput');
    const sessionInput = document.getElementById('sessionInput');
    const responseOutput = document.getElementById('responseOutput');
    const responseTime = document.getElementById('responseTime');
    const responseStatus = document.getElementById('responseStatus');
    
    const endpoint = endpointSelect.value;
    const method = endpoint.includes('/api/chat') ? 'POST' : 'GET';
    
    // ساخت درخواست
    const requestOptions = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    // اضافه کردن body برای endpointهای POST
    if (method === 'POST') {
        const body = {
            message: messageInput.value || 'سلام تست'
        };
        
        // اضافه کردن session_id برای chat-memory
        if (endpoint === '/api/chat-memory' && sessionInput.value) {
            body.session_id = sessionInput.value;
        }
        
        requestOptions.body = JSON.stringify(body);
    }
    
    // نمایش حالت لودینگ
    responseOutput.textContent = 'در حال ارسال درخواست...';
    responseStatus.textContent = 'در حال پردازش';
    responseStatus.style.color = '#f8961e';
    
    try {
        const startTime = Date.now();
        const response = await fetch(`${API_BASE_URL}${endpoint}`, requestOptions);
        const endTime = Date.now();
        
        const data = await response.json();
        const responseTimeMs = endTime - startTime;
        
        // به‌روزرسانی UI
        responseTime.textContent = responseTimeMs;
        responseStatus.textContent = response.ok ? 'موفق' : 'خطا';
        responseStatus.style.color = response.ok ? '#4cc9f0' : '#f72585';
        
        // نمایش پاسخ با فرمت زیبا
        responseOutput.textContent = JSON.stringify(data, null, 2);
        
        // اعلان موفقیت
        showNotification(`✅ درخواست با موفقیت اجرا شد (${responseTimeMs}ms)`, 'success');
        
    } catch (error) {
        console.error('خطا در تست API:', error);
        
        responseOutput.textContent = JSON.stringify({
            error: 'خطا در اتصال به سرور',
            message: error.message
        }, null, 2);
        
        responseStatus.textContent = 'خطا';
        responseStatus.style.color = '#f72585';
        
        showNotification('❌ خطا در اجرای درخواست', 'error');
    }
}

// کپی آدرس API
function copyUrl() {
    const url = document.getElementById('apiUrl').textContent;
    
    navigator.clipboard.writeText(url)
        .then(() => {
            showNotification('✅ آدرس API کپی شد', 'success');
        })
        .catch(err => {
            console.error('خطا در کپی:', err);
            showNotification('❌ خطا در کپی کردن', 'error');
        });
}

// نمایش اعلان
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    const notificationText = document.getElementById('notificationText');
    
    // تنظیم رنگ بر اساس نوع
    notification.style.background = type === 'success' ? '#4cc9f0' : 
                                  type === 'error' ? '#f72585' : '#4361ee';
    
    // نمایش اعلان
    notificationText.textContent = message;
    notification.classList.add('show');
    
    // مخفی کردن پس از 3 ثانیه
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// تولید session ID تصادفی
function generateSessionId() {
    return 'session_' + Math.random().toString(36).substr(2, 9);
}

// پر کردن فیلدهای تست با مقادیر پیش‌فرض
function fillTestData() {
    const messageInput = document.getElementById('messageInput');
    const sessionInput = document.getElementById('sessionInput');
    
    if (!messageInput.value) {
        messageInput.value = 'سلام! من از رابط کاربری شما تست می‌کنم.';
    }
    
    if (!sessionInput.value && document.getElementById('endpointSelect').value === '/api/chat-memory') {
        sessionInput.value = generateSessionId();
    }
}
