#!/bin/bash
clear
echo "🔄 راه‌اندازی مجدد natiq-ultimate..."

# پورت‌ها
UI_PORT=8080
API_PORT=8081

# توقف قبلی‌ها
pkill -f "uvicorn" 2>/dev/null
pkill -f "http.server" 2>/dev/null

# راه‌اندازی API
echo "🌐 راه‌اندازی API روی پورت $API_PORT..."
cd ~/natiq-ultimate
python3 simple_api.py &
sleep 3

# راه‌اندازی UI
echo "🎨 راه‌اندازی رابط کاربری روی پورت $UI_PORT..."
cd ~/natiq-ultimate/public
python3 -m http.server $UI_PORT --bind 127.0.0.1 &
sleep 2

# نمایش وضعیت
echo ""
echo "✅ سیستم آماده است!"
echo ""
echo "🔗 آدرس‌ها:"
echo "• رابط کاربری: http://localhost:$UI_PORT"
echo "• API: http://localhost:$API_PORT/api/health"
echo ""
echo "🧪 تست API:"
curl -s http://localhost:$API_PORT/api/health | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f'   وضعیت: {data.get(\"status\", \"?\")}')
    print(f'   نسخه: {data.get(\"version\", \"?\")}')
except:
    print('   ❌ API پاسخ نمی‌دهد')
"

echo ""
echo "📱 در مرورگر بروید به: http://localhost:$UI_PORT"
echo "🔄 صفحه را رفرش کنید (F5 یا Ctrl+F5)"
echo ""
echo "🛑 برای توقف: Ctrl+C"
echo ""

wait
