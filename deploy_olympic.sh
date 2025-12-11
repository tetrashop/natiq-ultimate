#!/bin/bash
# اسکریپت استقرار المپیکی ناتیق

echo "🏆 ==========================================="
echo "🏆 استقرار حالت المپیکی ناتیق اولتیمیت"
echo "🏆 ==========================================="

cd ~/natiq-ultimate

# مرحله ۱: پاکسازی
echo "🧹 مرحله ۱: پاکسازی محیط..."
rm -rf .vercel
rm -f api/*.pyc

# مرحله ۲: بررسی ساختار
echo "📁 مرحله ۲: بررسی ساختار پروژه..."
echo "--- ساختار فعلی ---"
find . -maxdepth 3 -type f -name "*.py" -o -name "*.json" -o -name "*.txt" -o -name "*.html" | grep -E "(api/|frontend/|vercel)" | sort

# مرحله ۳: تست محلی API
echo "🐍 مرحله ۳: تست محلی API..."
cd api
python3.9 -c "
import json
import sys

# شبیه‌سازی event
test_event = {
    'path': '/api/health',
    'httpMethod': 'GET',
    'body': '{}'
}

# اضافه کردن مسیر به sys.path
sys.path.insert(0, '.')

try:
    # import داینامیک هندلر
    import importlib.util
    spec = importlib.util.spec_from_file_location('handler', 'index.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # اجرای هندلر
    result = module.handler(test_event, None)
    
    print('✅ تست محلی موفقیت‌آمیز بود!')
    print(json.dumps(result, indent=2, ensure_ascii=False))
except Exception as e:
    print(f'❌ خطا در تست محلی: {e}')
    sys.exit(1)
"
cd ..

# مرحله ۴: استقرار
echo "🚀 مرحله ۴: استقرار روی Vercel..."
vercel --force --prod 2>&1 | tee deployment.log

# مرحله ۵: استخراج لینک
echo "🔗 مرحله ۵: استخراج لینک‌ها..."
PRODUCTION_URL=$(grep -o 'Production: .*' deployment.log | cut -d' ' -f2)
INSPECT_URL=$(grep -o 'Inspect: .*' deployment.log | cut -d' ' -f2)

if [ ! -z "$PRODUCTION_URL" ]; then
    echo ""
    echo "🎉 ==========================================="
    echo "🎉 استقرار با موفقیت انجام شد!"
    echo "🎉 ==========================================="
    echo ""
    echo "🌐 لینک تولید: $PRODUCTION_URL"
    echo "📊 لینک بازرسی: $INSPECT_URL"
    echo ""
    echo "🧪 تست‌های سریع:"
    echo "   سلامت API:   curl $PRODUCTION_URL/api/health"
    echo "   چت:          curl -X POST $PRODUCTION_URL/api/chat -H 'Content-Type: application/json' -d '{\"message\":\"سلام\"}'"
    echo "   رابط کاربری: open $PRODUCTION_URL"
    echo ""
    # ذخیره لینک‌ها
    echo "PRODUCTION_URL=$PRODUCTION_URL" > .deployment_info
    echo "INSPECT_URL=$INSPECT_URL" >> .deployment_info
else
    echo "❌ خطا در استقرار! لاگ را بررسی کنید."
    exit 1
fi

echo "🏆 فرآیند استقرار المپیکی تکمیل شد!"
