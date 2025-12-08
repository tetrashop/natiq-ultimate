#!/bin/bash
echo "🔍 تست کامل اتصال..."

# تست 1: API مستقیم
echo "1. تست API سرور:"
if curl -s http://localhost:8081/api/health > /dev/null; then
    echo "   ✅ API کار می‌کند"
    curl -s http://localhost:8081/api/health | python3 -c "import sys,json; print('   📊 پاسخ:', json.dumps(json.load(sys.stdin), indent=2, ensure_ascii=False))" 2>/dev/null
else
    echo "   ❌ API کار نمی‌کند"
fi

# تست 2: UI مستقیم
echo -e "\n2. تست UI سرور:"
if curl -s http://localhost:8080 > /dev/null; then
    echo "   ✅ UI کار می‌کند"
    echo "   📄 دریافت صفحه اصلی..."
    curl -s http://localhost:8080 | grep -o "<title>[^<]*" | head -1
else
    echo "   ❌ UI کار نمی‌کند"
fi

# تست 3: بررسی فایل‌های JS
echo -e "\n3. بررسی فایل‌های JavaScript:"
if [ -f ~/natiq-ultimate/public/assets/js/app.js ]; then
    echo "   ✅ فایل app.js وجود دارد"
    grep -n "localhost" ~/natiq-ultimate/public/assets/js/app.js | head -2
else
    echo "   ⚠️  فایل app.js یافت نشد"
fi

# تست 4: بررسی CORS
echo -e "\n4. تست CORS:"
curl -s -I http://localhost:8081/api/health | grep -i "access-control"

echo -e "\n🎯 نتیجه:"
if curl -s http://localhost:8081/api/health > /dev/null && curl -s http://localhost:8080 > /dev/null; then
    echo "✅ همه چیز به درستی کار می‌کند!"
    echo "📱 به آدرس http://localhost:8080 در مرورگر بروید"
else
    echo "⚠️  برخی بخش‌ها مشکل دارند"
fi
