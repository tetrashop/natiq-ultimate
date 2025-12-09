#!/bin/bash

echo "🚀 راه‌اندازی نطق مصطلح نسخه نهایی..."
echo "============================================="

# توقف سرورهای قبلی
pkill -f "node.*server" 2>/dev/null
sleep 2

# بررسی و بازیابی فایل package.json
if [ -f ~/package.json.backup ]; then
    echo "📦 بازیابی تنظیمات npm..."
    mv ~/package.json.backup ~/package.json 2>/dev/null || true
fi

# راه‌اندازی سرور اصلی
cd ~/natiq-ultimate
echo "🌐 راه‌اندازی سرور روی پورت 3001..."
node super-simple-server.js > natiq.log 2>&1 &
SERVER_PID=$!

sleep 3

# بررسی سلامت
echo "🏥 بررسی سلامت سیستم..."
HEALTH=$(curl -s http://localhost:3003/api/health 2>/dev/null || echo "{}")
if echo "$HEALTH" | grep -q "healthy"; then
    echo "✅ سیستم سالم است!"
    echo "📊 مقالات: $(echo "$HEALTH" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('articles', {}).get('total', 0))")"
else
    echo "⚠️  مشکل در سلامت سیستم"
    tail -10 natiq.log
fi

# تست جستجو
echo "🔍 تست سیستم جستجو..."
SEARCH_RESULT=$(curl -s "http://localhost:3003/api/search?q=پردازش")
if [ -n "$SEARCH_RESULT" ]; then
    echo "✅ جستجو پاسخ داد"
    echo "   نتایج: $(echo "$SEARCH_RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('totalResults', 0))" 2>/dev/null || echo "N/A")"
else
    echo "⚠️  جستجو پاسخی نداد"
fi

echo ""
echo "============================================="
echo "🎉 نطق مصطلح راه‌اندازی شد!"
echo "🌐 آدرس‌ها:"
echo "   وب‌اپلیکیشن: http://localhost:3003"
echo "   API سلامت: http://localhost:3003/api/health"
echo "   API جستجو: http://localhost:3003/api/search?q=پردازش"
echo "   API مقالات: http://localhost:3003/api/articles"
echo ""
echo "📋 لاگ سیستم: tail -f ~/natiq-ultimate/natiq.log"
echo "🛑 توقف: pkill -f 'node.*super-simple'"
echo "============================================="

# ذخیره PID
echo $SERVER_PID > ~/natiq-ultimate/server.pid
