#!/bin/bash

# پورت‌های جدید - از پورت‌های رایج استفاده می‌کنیم
UI_PORT=8080    # پورت جایگزین برای رابط کاربری
API_PORT=8081   # پورت جایگزین برای API

echo "🔄 راه‌اندازی natiq-ultimate با پورت‌های جدید..."
echo "🎨 رابط کاربری: پورت $UI_PORT"
echo "🌐 API: پورت $API_PORT"

# توقف سرورهای قبلی
echo "⏹ توقف سرورهای قبلی..."
pkill -f "uvicorn" 2>/dev/null
pkill -f "http.server" 2>/dev/null
sleep 2

# راه‌اندازی API
echo "🌐 راه‌اندازی API روی پورت $API_PORT..."
cd ~/natiq-ultimate
python3 -m uvicorn api.index:app --host 0.0.0.0 --port $API_PORT > api_$API_PORT.log 2>&1 &
API_PID=$!
sleep 3

# راه‌اندازی UI
echo "🎨 راه‌اندازی رابط کاربری روی پورت $UI_PORT..."
cd ~/natiq-ultimate/public
python3 -m http.server $UI_PORT > ui_$UI_PORT.log 2>&1 &
UI_PID=$!
sleep 2

# نمایش اطلاعات
echo ""
echo "========================================"
echo "✅ سیستم با موفقیت راه‌اندازی شد!"
echo ""
echo "📱 در مرورگر باز کنید:"
echo "• رابط کاربری: http://localhost:$UI_PORT"
echo "• یا: http://127.0.0.1:$UI_PORT"
echo ""
echo "🔧 تست API:"
echo "• سلامت سیستم: http://localhost:$API_PORT/api/health"
echo "• دانش پایه: http://localhost:$API_PORT/api/knowledge"
echo ""
echo "📊 لاگ‌ها:"
echo "• API: ~/natiq-ultimate/api_$API_PORT.log"
echo "• UI: ~/natiq-ultimate/public/ui_$UI_PORT.log"
echo ""
echo "🎮 مدیریت:"
echo "• مشاهده لاگ API: tail -f api_$API_PORT.log"
echo "• مشاهده لاگ UI: tail -f public/ui_$UI_PORT.log"
echo "• توقف: pkill -f 'uvicorn|http.server'"
echo "========================================"
echo ""

# نگه داشتن اسکریپت
echo "برای توقف سیستم، Ctrl+C را فشار دهید..."
wait
