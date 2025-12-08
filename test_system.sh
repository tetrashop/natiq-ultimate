#!/bin/bash

echo "🧪 تست کامل سیستم natiq-ultimate..."

# 1. بررسی ساختار
echo "1. بررسی ساختار پروژه..."
ls -la public/ index.html 2>/dev/null || echo "❌ فایل index.html در مسیر اصلی نیست"
ls -la api/index.py 2>/dev/null || echo "⚠️  فایل api/index.py ممکن است مشکل داشته باشد"

# 2. بررسی API
echo "2. تست API..."
if command -v python3 &> /dev/null; then
    python3 << 'PYEOF'
import sys
import os
sys.path.append(os.path.expanduser('~/natiq-ultimate'))

try:
    import fastapi
    print("✅ FastAPI نصب شده است")
except ImportError:
    print("❌ FastAPI نصب نیست. نصب کنید: pip install fastapi uvicorn")
PYEOF
else
    echo "⚠️  پایتون 3 یافت نشد"
fi

# 3. راه‌اندازی تست
echo "3. راه‌اندازی تست سرور..."
cd ~/natiq-ultimate
timeout 5 python3 -m uvicorn api.index:app --host 127.0.0.1 --port 9999 > /tmp/test_server.log 2>&1 &
SERVER_PID=$!
sleep 3

# 4. تست اتصال
echo "4. تست اتصال به سرور..."
if curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:9999/api/health 2>/dev/null | grep -q "200"; then
    echo "✅ اتصال به API موفقیت‌آمیز"
    echo "📊 پاسخ API:"
    curl -s http://127.0.0.1:9999/api/health | python3 -m json.tool 2>/dev/null || curl -s http://127.0.0.1:9999/api/health
else
    echo "❌ اتصال به API ناموفق"
    echo "📄 لاگ سرور:"
    cat /tmp/test_server.log
fi

kill $SERVER_PID 2>/dev/null

# 5. پیشنهادات
echo ""
echo "🎯 پیشنهادات:"
echo "• اگر API کار می‌کند: python3 -m uvicorn api.index:app --host 0.0.0.0 --port 8000"
echo "• اگر API مشکل دارد: cd public && python3 -m http.server 3000"
echo "• برای رابط کاربری: مرورگر را باز کنید و به آدرس بالا بروید"
