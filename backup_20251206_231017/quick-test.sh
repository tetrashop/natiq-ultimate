#!/bin/bash

echo "⚡ تست سریع نطق مصطلح"
echo "===================="

# تست سلامت
echo -e "\n1. سلامت سرور مقالات:"
if curl -s "http://localhost:3000/api/health" > /dev/null; then
    echo "   ✅ سرور مقالات فعال"
else
    echo "   ❌ سرور مقالات غیرفعال"
fi

echo -e "\n2. سلامت سرور پرسش و پاسخ:"
if curl -s "http://localhost:3002/api/qna/health" > /dev/null; then
    echo "   ✅ سرور پرسش و پاسخ فعال"
else
    echo "   ❌ سرور پرسش و پاسخ غیرفعال"
fi

echo -e "\n3. تست پرسش ساده:"
curl -G "http://localhost:3002/api/qna/ask" \
  --data-urlencode "q=آیا سیستم کار می‌کند؟" \
  --silent | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if data.get('success'):
        print(f'   ✅ بله! سیستم پاسخ داد: {data.get(\"confidence\", 0)}% اعتماد')
    else:
        print(f'   ❌ خطا: {data.get(\"error\", \"خطا\")}')
except:
    print('   ❌ خطای ارتباطی')
"

echo -e "\n4. تست مقاله 203:"
curl -s "http://localhost:3000/api/article/203" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if data.get('success'):
        print(f'   ✅ مقاله 203 موجود است')
    else:
        print(f'   ❌ مقاله 203 یافت نشد')
except:
    print('   ❌ خطای ارتباطی')
"

echo -e "\n===================="
echo "🌐 آدرس‌های تست:"
echo "   مقالات: http://localhost:3000"
echo "   پرسش و پاسخ: http://localhost:3002"
echo "   تست رابط: file:///data/data/com.termux/files/home/natiq-ultimate/test-qna.html"
