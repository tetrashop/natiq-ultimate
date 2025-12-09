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

# 3. ایجاد پوشه‌ها
echo "📁 ایجاد پوشه‌های پروژه..."
mkdir -p api logs data config translations
mkdir -p logs/api data/users config/project translations/{fa,en,ar}

# 4. اجرای تست‌ها
echo "🧪 اجرای تست‌ها..."
python3 test_file_processor.py

# 5. بررسی ساختار
echo "📁 ساختار پروژه:"
find . -type f -name "*.py" | sort

echo ""
echo "✅ نصب با موفقیت کامل شد!"
echo "🔍 برای استفاده، فایل advanced_file_processor.py را import کنید:"
echo "   from advanced_file_processor import cat, FileProcessor"
