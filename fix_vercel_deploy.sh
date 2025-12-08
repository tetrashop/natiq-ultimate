#!/bin/bash
echo "🔧 اصلاح پروژه برای Vercel..."

cd ~/natiq-ultimate

# 1. اصلاح app.js
echo "1. اصلاح app.js..."
sed -i "s|http://localhost:8081|window.location.origin|g" public/assets/js/app.js
sed -i "s|fetch('/api/health|fetch(window.location.origin + '/api/health|g" public/assets/js/app.js

# 2. اصلاح chat.js
echo "2. اصلاح chat.js..."
if [ -f "public/assets/js/chat.js" ]; then
    sed -i "s|this.apiBase = 'http://localhost:8081'|this.apiBase = window.location.origin|g" public/assets/js/chat.js
    sed -i "s|\${this.apiBase}/api/ask|window.location.origin + '/api/ask'|g" public/assets/js/chat.js
fi

# 3. ایجاد فایل config
echo "3. ایجاد فایل پیکربندی..."
cat > public/assets/js/config.js << 'CONFIGEOF'
// پیکربندی API برای محیط‌های مختلف
const CONFIG = {
    IS_PRODUCTION: window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1',
    
    getApiUrl: function(path) {
        if (this.IS_PRODUCTION) {
            return window.location.origin + path;
        } else {
            // در توسعه، از localhost:8081 استفاده کن
            return 'http://localhost:8081' + path;
        }
    }
};
CONFIGEOF

# 4. به‌روزرسانی index.html
echo "4. اضافه کردن config.js به index.html..."
if grep -q "config.js" public/index.html; then
    echo "config.js already exists in index.html"
else
    # اضافه کردن قبل از app.js
    sed -i '/<script src="\/assets\/js\/app.js"/i\    <script src="/assets/js/config.js"></script>' public/index.html
fi

# 5. Push به GitHub
echo "5. ارسال تغییرات به GitHub..."
git add .
git commit -m "fix: اصلاح آدرس API برای سازگاری با Vercel

• تغییر آدرس API از localhost به window.location.origin
• اضافه کردن فایل پیکربندی محیط‌های مختلف
• بهبود مدیریت CORS
• آماده برای دیپلوی روی Vercel"

git push origin main

echo ""
echo "✅ تغییرات اعمال شد!"
echo "🌐 حالا به Vercel بروید و دکمه Redeploy را بزنید"
echo "📱 آدرس Vercel شما: https://natiq-ultimate.vercel.app"
