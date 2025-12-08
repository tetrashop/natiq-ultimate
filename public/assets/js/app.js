// توابع کلی برنامه
function toggleTheme() {
    const body = document.body;
    const themeIcon = document.querySelector('.theme-toggle i');
    
    if (body.classList.contains('light-mode')) {
        body.classList.replace('light-mode', 'dark-mode');
        themeIcon.classList.replace('fa-moon', 'fa-sun');
        localStorage.setItem('theme', 'dark');
    } else {
        body.classList.replace('dark-mode', 'light-mode');
        themeIcon.classList.replace('fa-sun', 'fa-moon');
        localStorage.setItem('theme', 'light');
    }
}

// بارگذاری وضعیت سیستم
async function loadSystemStatus() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        if (data.status === 'healthy') {
            document.getElementById('systemStatus').innerText = 'فعال';
            document.getElementById('systemStatus').className = 'status-badge active';
            
            if (data.knowledge_count !== undefined) {
                document.getElementById('knowledgeCount').innerText = data.knowledge_count;
            }
            
            // به‌روزرسانی وضعیت فوتر
            const footerStatus = document.querySelector('.status-indicator .status-dot');
            if (footerStatus) {
                footerStatus.classList.add('active');
            }
        } else {
            document.getElementById('systemStatus').innerText = 'مشکل دارد';
            document.getElementById('systemStatus').className = 'status-badge status-error';
        }
    } catch (error) {
        console.error('خطا در دریافت وضعیت سیستم:', error);
        document.getElementById('systemStatus').innerText = 'قطع ارتباط';
        document.getElementById('systemStatus').className = 'status-badge status-error';
    }
}

// نمایش توستر
function showToast(message, type = 'info', duration = 5000) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
    }, duration);
}

// بارگذاری اولیه
document.addEventListener('DOMContentLoaded', function() {
    // اعمال تم ذخیره شده
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (savedTheme === 'dark') {
        document.body.classList.replace('light-mode', 'dark-mode');
        document.querySelector('.theme-toggle i').classList.replace('fa-moon', 'fa-sun');
    }
    
    // بارگذاری وضعیت سیستم
    loadSystemStatus();
    
    // به‌روزرسانی دوره‌ای وضعیت
    setInterval(loadSystemStatus, 60000); // هر 1 دقیقه
    
    // نمایش شناسه جلسه
    const sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    document.getElementById('sessionId').innerText = sessionId;
    
    // تنظیم event listener برای لینک‌ها
    document.querySelectorAll('a[target="_api"]').forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('آیا می‌خواهید این endpoint را در تب جدید باز کنید؟')) {
                e.preventDefault();
            }
        });
    });
    
    console.log('natiq-ultimate v6.0 Frontend loaded successfully!');
});

// توابع کمکی
function formatDate(date) {
    return new Intl.DateTimeFormat('fa-IR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// پشتیبانی از کلیپ‌بورد
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('متن با موفقیت کپی شد', 'success');
    }).catch(err => {
        console.error('خطا در کپی کردن:', err);
        showToast('خطا در کپی کردن متن', 'error');
    });
}
