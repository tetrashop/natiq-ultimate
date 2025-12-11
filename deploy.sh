#!/bin/bash

echo "🚀 استقرار ساده ناتیق اولتیمیت"
echo "============================="

# بررسی وجود فایل‌های ضروری
if [ ! -f "vercel.json" ]; then
    echo "❌ فایل vercel.json یافت نشد"
    exit 1
fi

if [ ! -f "api/index.js" ]; then
    echo "❌ فایل api/index.js یافت نشد"
    exit 1
fi

# نصب و راه‌اندازی Vercel
echo "📦 بررسی Vercel CLI..."
if ! command -v vercel &> /dev/null; then
    echo "⚠️  Vercel CLI نصب نیست"
    echo "📥 نصب با: npm install -g vercel"
    npm install -g vercel
fi

# استقرار
echo "🚀 شروع استقرار..."
vercel --prod --confirm --yes --token=$(vercel token 2>/dev/null || echo "")

if [ $? -eq 0 ]; then
    echo "✅ استقرار موفقیت‌آمیز بود!"
    echo ""
    echo "📋 راهنمای پس از استقرار:"
    echo "1. به Vercel Dashboard بروید"
    echo "2. پروژه را انتخاب کنید"
    echo "3. به Settings → Authentication بروید"
    echo "4. 'Enable Authentication' را غیرفعال کنید"
    echo ""
    echo "🌐 تست سیستم:"
    echo "curl https://your-project.vercel.app/api/health"
else
    echo "❌ استقرار ناموفق بود"
fi
