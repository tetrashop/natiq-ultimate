#!/bin/bash
cd ~/natiq-ultimate

echo "🔄 توقف سرویس‌های قبلی..."
pkill -f "uvicorn" 2>/dev/null
pkill -f "http.server" 2>/dev/null
pkill -f "simple_api.py" 2>/dev/null
sleep 2

echo "📝 ایجاد فایل API ساده..."
cat > simple_api.py << 'PYEOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "version": "6.0",
        "knowledge_count": 15,
        "timestamp": "2024-12-08",
        "message": "natiq-ultimate v6.0 - سیستم عصبی نمادین"
    }

@app.get("/api/knowledge")
async def knowledge():
    return {
        "success": True,
        "count": 15,
        "knowledge": [
            {"id": 1, "question": "AI چیست؟", "answer": "هوش مصنوعی"},
            {"id": 2, "question": "NLP چیست؟", "answer": "پردازش زبان طبیعی"}
        ]
    }

@app.get("/")
async def root():
    return {"message": "API Server is running"}

if __name__ == "__main__":
    print("🚀 API سرور روی پورت 8081 راه‌اندازی شد")
    uvicorn.run(app, host="127.0.0.1", port=8081, log_level="info")
PYEOF

echo "🔧 ایجاد فایل JavaScript به‌روز شده..."
mkdir -p public/assets/js

cat > public/assets/js/app.js << 'JSEOF'
// توابع کلی برنامه
async function loadSystemStatus() {
    try {
        console.log('درخواست وضعیت سیستم...');
        const response = await fetch('http://localhost:8081/api/health');
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
JSEOF

echo "🚀 راه‌اندازی سرورها..."
# راه‌اندازی API
python3 simple_api.py &
sleep 3

# راه‌اندازی UI
cd ~/natiq-ultimate/public
python3 -m http.server 8080 --bind 127.0.0.1 &
sleep 2

echo ""
echo "🎉 ========================================="
echo "✅ سیستم natiq-ultimate راه‌اندازی شد!"
echo ""
echo "🌐 آدرس‌های دسترسی:"
echo "   🔗 رابط کاربری: http://localhost:8080"
echo "   🔗 API سلامت: http://localhost:8081/api/health"
echo "   🔗 API دانش: http://localhost:8081/api/knowledge"
echo ""
echo "📱 در مرورگر Android:"
echo "   1. Chrome یا Firefox را باز کنید"
echo "   2. آدرس: http://localhost:8080"
echo "   3. یا: http://127.0.0.1:8080"
echo ""
echo "🔧 مدیریت:"
echo "   • توقف: pkill -f 'python'"
echo "   • وضعیت: ps aux | grep python"
echo "=========================================="
echo ""

# نگه داشتن اسکریپت
echo "برای توقف سیستم، Ctrl+C را فشار دهید..."
wait
