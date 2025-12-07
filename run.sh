#!/bin/bash
# اسکریپت اجرای سریع natiq-ultimate

echo "🚀 راه‌اندازی natiq-ultimate"
echo "================================"

# بررسی پایتون
if ! command -v python3 &> /dev/null; then
    echo "❌ پایتون یافت نشد!"
    exit 1
fi

# بررسی کتابخانه‌ها
echo "📦 بررسی نیازمندی‌ها..."
python3 -c "
import sys
print(f'پایتون {sys.version}')

libs = ['torch', 'transformers', 'numpy']
for lib in libs:
    try:
        __import__(lib)
        print(f'✅ {lib} نصب است')
    except ImportError:
        print(f'❌ {lib} یافت نشد')
"

# اجرای تست
echo ""
echo "🧪 اجرای تست سیستم..."
python3 src/test_nlp.py
