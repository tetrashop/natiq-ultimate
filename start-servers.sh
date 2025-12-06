#!/bin/bash

cd ~/natiq-ultimate

echo "🛑 متوقف کردن سرورهای قبلی..."
pkill -f "node" 2>/dev/null
sleep 2

echo "🚀 راه‌اندازی سرور اصلی مقالات (پورت 3000)..."
node natiq-complete.cjs &
sleep 3

echo "🧠 راه‌اندازی سرور پرسش و پاسخ (پورت 3002)..."
node qna-server.cjs &
sleep 3

echo -e "\n✅ سرورها راه‌اندازی شدند!"
echo "🌐 آدرس‌ها:"
echo "   مقالات: http://localhost:3000"
echo "   پرسش و پاسخ: http://localhost:3002"
echo "   تست رابط: file://$(pwd)/test-qna.html"
echo -e "\n📊 وضعیت سرورها:"

# تست سلامت
curl -s "http://localhost:3000/api/health" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'📚 سرور مقالات: {data[\"articles\"]} مقاله - {data[\"status\"]}')
" 2>/dev/null || echo "❌ سرور مقالات پاسخ نمی‌دهد"

curl -s "http://localhost:3002/api/qna/health" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'🧠 سرور پرسش و پاسخ: {data[\"faqCount\"]} سوال - {data[\"status\"]}')
" 2>/dev/null || echo "❌ سرور پرسش و پاسخ پاسخ نمی‌دهد"
