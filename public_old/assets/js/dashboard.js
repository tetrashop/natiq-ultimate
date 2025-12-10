// توابع داشبورد
async function testAPI(endpoint) {
    try {
        showToast(`در حال تست ${endpoint}...`, 'info');
        
        const response = await fetch(endpoint);
        const data = await response.json();
        
        const responseElement = document.getElementById('apiResponse');
        responseElement.textContent = JSON.stringify(data, null, 2);
        responseElement.style.color = '#28a745';
        
        showToast('تست API موفقیت‌آمیز بود', 'success');
    } catch (error) {
        const responseElement = document.getElementById('apiResponse');
        responseElement.textContent = `خطا: ${error.message}`;
        responseElement.style.color = '#dc3545';
        
        showToast('خطا در تست API', 'error');
    }
}

// بارگذاری آمار داشبورد
async function loadDashboardStats() {
    try {
        const healthResponse = await fetch('/api/health');
        const healthData = await healthResponse.json();
        
        if (healthData.knowledge_count) {
            document.getElementById('dashboardKnowledgeCount').textContent = healthData.knowledge_count;
        }
        
        // بارگذاری آمار از localStorage
        const stats = JSON.parse(localStorage.getItem('natiq_stats') || '{}');
        if (stats.count) {
            document.getElementById('totalConversations').textContent = stats.count;
        }
        
        // بارگذاری جلسات ذخیره شده
        const sessions = JSON.parse(localStorage.getItem('natiq_sessions') || '[]');
        if (sessions.length > 0) {
            console.log(`تعداد جلسات ذخیره شده: ${sessions.length}`);
        }
    } catch (error) {
        console.error('خطا در بارگذاری آمار:', error);
    }
}

// بارگذاری اولیه داشبورد
document.addEventListener('DOMContentLoaded', function() {
    loadDashboardStats();
    
    // به‌روزرسانی دوره‌ی آمار
    setInterval(loadDashboardStats, 30000); // هر 30 ثانیه
    
    // تنظیم event listener برای دکمه‌ها
    document.querySelectorAll('.test-buttons button').forEach(button => {
        button.addEventListener('click', function() {
            const endpoint = this.getAttribute('onclick').match(/'([^']+)'/)[1];
            testAPI(endpoint);
        });
    });
});
