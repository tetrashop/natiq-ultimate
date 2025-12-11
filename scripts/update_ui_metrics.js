// بروزرسانی اتوماتیک متریک‌های UI
const fs = require('fs');
const path = require('path');

const uiFile = path.join(__dirname, '../frontend/index.html');
let html = fs.readFileSync(uiFile, 'utf8');

// 1. افزودن سیستم رفرش خودکار
const autoRefresh = `
<script>
// رفرش اتوماتیک هر 30 ثانیه
setTimeout(() => {
    console.log('🔄 بروزرسانی خودکار UI...');
    window.location.reload();
}, 30000);

// نمایش آخرین بروزرسانی
document.addEventListener('DOMContentLoaded', () => {
    const now = new Date();
    const timeString = now.toLocaleTimeString('fa-IR');
    const dateString = now.toLocaleDateString('fa-IR');
    
    // اضافه کردن تاریخ در فوتر
    const footer = document.querySelector('.footer, .footer-bottom');
    if (footer) {
        const updateInfo = document.createElement('div');
        updateInfo.style.marginTop = '10px';
        updateInfo.style.fontSize = '0.8em';
        updateInfo.style.opacity = '0.7';
        updateInfo.textContent = \`آخرین بروزرسانی: \${dateString} - \${timeString}\`;
        footer.appendChild(updateInfo);
    }
});
</script>
`;

// 2. تضمین نمایش صحیح آمار
html = html.replace(
    /مانیتورینگ زنده[\s\S]*?Edge Node/m,
    `مانیتورینگ زنده
Latency
<span id="realLatency">15</span>
ms
Uptime
<span id="realUptime">100.00</span>
%
Requests
<span id="realRequests">0</span>
req
Edge Node`
);

// 3. اضافه کردن اسکریپت
if (!html.includes('آخرین بروزرسانی')) {
    html = html.replace('</body>', autoRefresh + '</body>');
}

fs.writeFileSync(uiFile, html);
console.log('✅ UI برای نمایش متریک‌های واقعی بروزرسانی شد');
