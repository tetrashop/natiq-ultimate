#!/bin/bash

cd ~/natiq-ultimate

echo "🛑 متوقف کردن سرورهای قبلی..."
pkill -f "node" 2>/dev/null
sleep 2

echo "🚀 راه‌اندازی سرور مقالات (پورت 3000)..."
node natiq-complete.cjs &
sleep 3

echo "🧠 راه‌اندازی سرور پرسش و پاسخ اصلاح شده (پورت 3002)..."
node qna-server-fixed.cjs &
sleep 3

echo -e "\n✅ سرورها راه‌اندازی شدند!"
echo "🌐 آدرس‌ها:"
echo "   📚 مقالات: http://localhost:3000"
echo "   🧠 پرسش و پاسخ: http://localhost:3002"
echo "   🖥️  تست رابط: file://$(pwd)/test-qna-fixed.html"
echo -e "\n📞 تست سریع:"
echo "   curl -G \"http://localhost:3002/api/qna/ask\" --data-urlencode \"q=پردازش زبان طبیعی چیست؟\""
