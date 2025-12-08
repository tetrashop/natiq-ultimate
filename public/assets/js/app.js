// توابع کلی برنامه
async function loadSystemStatus() {
    try {
        console.log('درخواست وضعیت سیستم...');
        const response = await fetch('window.location.origin/api/health');
        const data = await response.json();
        
        const statusElement = document.getElementById('systemStatus');
        const knowledgeElement = document.getElementById('knowledgeCount');
        
        if (data.status === 'healthy') {
            statusElement.innerText = 'فعال';
            statusElement.className = 'status-badge active';
            knowledgeElement.innerText = data.knowledge_count || 10;
            console.log('✅ سیستم سالم است');
        } else {
            statusElement.innerText = 'مشکل دارد';
            statusElement.className = 'status-badge status-error';
            console.error('سیستم مشکل دارد:', data);
        }
    } catch (error) {
        console.error('خطا در دریافت وضعیت:', error);
        document.getElementById('systemStatus').innerText = 'قطع ارتباط';
        document.getElementById('systemStatus').className = 'status-badge status-error';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('صفحه بارگذاری شد');
    loadSystemStatus();
    
    // تم تاریک/روشن
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            document.body.classList.toggle('light-mode');
        });
    }
});
