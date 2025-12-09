#!/bin/bash
# اسکریپت نصب سریع الگوریتم مدیریت فایل

echo "🔧 شروع نصب الگوریتم مدیریت فایل پیشرفته"
echo "=========================================="

# 1. بررسی وجود پایتون
if ! command -v python3 &> /dev/null; then
    echo "❌ پایتون 3 یافت نشد!"
    exit 1
fi

# 2. نصب وابستگی‌ها
echo "📦 نصب وابستگی‌ها..."
pip install PyYAML python-multipart

# 3. ایجاد فایل‌ها
echo "📝 ایجاد فایل‌های الگوریتم..."

# ایجاد فایل advanced_file_processor.py
cat > advanced_file_processor.py << 'PYEOF'
[محتوای advanced_file_processor.py اینجا کپی شود]
PYEOF

# ایجاد فایل test_file_processor.py
cat > test_file_processor.py << 'PYEOF'
[محتوای test_file_processor.py اینجا کپی شود]
PYEOF

# 4. به‌روزرسانی requirements.txt
echo "📋 به‌روزرسانی فایل نیازمندی‌ها..."
if [ -f requirements.txt ]; then
    if ! grep -q "PyYAML" requirements.txt; then
        echo "PyYAML==6.0.1" >> requirements.txt
    fi
    if ! grep -q "python-multipart" requirements.txt; then
        echo "python-multipart==0.0.6" >> requirements.txt
    fi
else
    echo "fastapi==0.104.1" > requirements.txt
    echo "uvicorn==0.24.0" >> requirements.txt
    echo "openai" >> requirements.txt
    echo "PyYAML==6.0.1" >> requirements.txt
    echo "python-multipart==0.0.6" >> requirements.txt
fi

# 5. اجرای تست‌ها
echo "🧪 اجرای تست‌ها..."
python3 test_file_processor.py

# 6. بررسی ساختار
echo "📁 ساختار پروژه:"
ls -la

echo ""
echo "✅ نصب با موفقیت کامل شد!"
echo "🔍 برای استفاده، فایل advanced_file_processor.py را import کنید:"
echo "   from advanced_file_processor import cat, FileProcessor"
