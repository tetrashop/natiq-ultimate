#!/bin/bash
echo "🎯 استقرار نهایی و قطعی سیستم ناتیق الماس"
echo "========================================"

# 1. حذف کش build
rm -rf .vercel 2>/dev/null

# 2. استقرار با تنظیمات دقیق
echo "🚀 در حال استقرار..."
DEPLOY_OUTPUT=$(vercel --prod --yes --confirm 2>&1)

# 3. بررسی نتیجه
if echo "$DEPLOY_OUTPUT" | grep -q "Production:"; then
    echo "✅ استقرار موفقیت‌آمیز بود!"
    
    # استخراج URL
    PRODUCTION_URL=$(echo "$DEPLOY_OUTPUT" | grep -o "Production: https://[^ ]*" | cut -d' ' -f2)
    echo "🌐 آدرس جدید: $PRODUCTION_URL"
    
    # اگر با دامنه اصلی متفاوت است، alias تنظیم کن
    if [[ "$PRODUCTION_URL" != *"natiq-ultimate.vercel.app"* ]]; then
        echo "🔗 تنظیم alias برای دامنه اصلی..."
        vercel alias set "$PRODUCTION_URL" natiq-ultimate.vercel.app 2>/dev/null || true
    fi
    
else
    echo "❌ خطا در استقرار"
    echo "$DEPLOY_OUTPUT" | tail -20
fi

echo ""
echo "📋 تست نهایی:"
echo "1. curl -s 'https://natiq-ultimate.vercel.app/api/health' | grep -o '\"status\":\"[^\"]*\"'"
echo "2. باز کردن https://natiq-ultimate.vercel.app در مرورگر و بررسی console (F12)"
