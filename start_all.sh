#!/bin/bash

echo "🚀 راه‌اندازی کامل natiq-ultimate..."

# پورت‌ها
API_PORT=8000
UI_PORT=3000

# توقف سرورهای قبلی
echo "⏹ توقف سرورهای قبلی..."
pkill -f "uvicorn" 2>/dev/null
pkill -f "http.server" 2>/dev/null

# راه‌اندازی API
echo "🌐 راه‌اندازی API روی پورت $API_PORT..."
cd ~/natiq-ultimate
python3 -m uvicorn api.index:app --host 0.0.0.0 --port $API_PORT > api.log 2>&1 &
API_PID=$!
sleep 3

# راه‌اندازی UI
echo "🎨 راه‌اندازی رابط کاربری روی پورت $UI_PORT..."
cd ~/natiq-ultimate/public
python3 -m http.server $UI_PORT > ui.log 2>&1 &
UI_PID=$!
sleep 2

# نمایش اطلاعات
echo ""
echo "========================================"
echo "✅ سیستم با موفقیت راه‌اندازی شد!"
echo ""
echo "🔗 لینک‌های دسترسی:"
echo "• رابط کاربری: http://localhost:$UI_PORT"
echo "• API سلامت: http://localhost:$API_PORT/api/health"
echo "• API دانش: http://localhost:$API_PORT/api/knowledge"
echo ""
echo "📊 لاگ‌ها:"
echo "• API: ~/natiq-ultimate/api.log"
echo "• UI: ~/natiq-ultimate/public/ui.log"
echo ""
echo "🎮 دستورات مدیریت:"
echo "• مشاهده لاگ API: tail -f api.log"
echo "• مشاهده لاگ UI: tail -f public/ui.log"
echo "• توقف همه: pkill -f 'uvicorn|http.server'"
echo "========================================"
echo ""

# نگه داشتن اسکریپت
echo "برای توقف، Ctrl+C را فشار دهید..."
wait
