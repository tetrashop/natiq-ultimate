#!/bin/bash

echo "🚀 شروع تست خودکار نطق مصطلح"
echo "============================="

# 1. بررسی وضعیت سرور
echo -e "\n1. 📡 بررسی وضعیت سرور..."
if curl -s "http://localhost:3000/api/health" > /dev/null; then
    echo "   ✅ سرور فعال است"
else
    echo "   ❌ سرور غیرفعال است"
    exit 1
fi

# 2. تست سلامت
echo -e "\n2. 🏥 تست سلامت API..."
HEALTH=$(curl -s "http://localhost:3000/api/health")
if echo "$HEALTH" | grep -q '"status"'; then
    ARTICLES=$(echo "$HEALTH" | python3 -c "import json,sys; print(json.load(sys.stdin)['articles'])")
    echo "   ✅ سیستم سالم - $ARTICLES مقاله"
else
    echo "   ❌ خطا در تست سلامت"
fi

# 3. تست مقاله 203
echo -e "\n3. 🎯 تست مقاله 203..."
ARTICLE=$(curl -s "http://localhost:3000/api/article/203")
if echo "$ARTICLE" | grep -q '"id": 203'; then
    TITLE=$(echo "$ARTICLE" | python3 -c "import json,sys; print(json.load(sys.stdin)['article']['title'][:50])")
    echo "   ✅ مقاله 203 موجود - '$TITLE...'"
else
    echo "   ❌ مقاله 203 یافت نشد"
fi

# 4. تست جستجو
echo -e "\n4. 🔍 تست جستجوی NLP..."
SEARCH=$(curl -s "http://localhost:3000/api/search?q=NLP")
if echo "$SEARCH" | grep -q '"success": true'; then
    COUNT=$(echo "$SEARCH" | python3 -c "import json,sys; print(json.load(sys.stdin)['totalResults'])")
    echo "   ✅ $COUNT نتیجه برای NLP یافت شد"
else
    echo "   ❌ خطا در جستجو"
fi

# 5. تست آمار
echo -e "\n5. 📊 تست آمار سیستم..."
STATS=$(curl -s "http://localhost:3000/api/stats")
if echo "$STATS" | grep -q '"success": true'; then
    VIEWS=$(echo "$STATS" | python3 -c "import json,sys; print('{:,}'.format(json.load(sys.stdin)['totalViews']))")
    LIKES=$(echo "$STATS" | python3 -c "import json,sys; print('{:,}'.format(json.load(sys.stdin)['totalLikes']))")
    echo "   ✅ بازدید کل: $VIEWS - لایک کل: $LIKES"
else
    echo "   ❌ خطا در دریافت آمار"
fi

# 6. تست لیست مقالات
echo -e "\n6. 📄 تست لیست مقالات..."
ARTICLES_LIST=$(curl -s "http://localhost:3000/api/articles?page=1&limit=3")
if echo "$ARTICLES_LIST" | grep -q '"success": true'; then
    COUNT=$(echo "$ARTICLES_LIST" | python3 -c "import json,sys; print(len(json.load(sys.stdin)['articles']))")
    echo "   ✅ $COUNT مقاله دریافت شد"
    
    # نمایش عناوین
    echo "$ARTICLES_LIST" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for i, article in enumerate(data['articles'], 1):
    print(f'      {i}. {article[\"title\"][:40]}...')
"
else
    echo "   ❌ خطا در دریافت مقالات"
fi

echo -e "\n============================="
echo "✅ تست خودکار کامل شد"
echo -e "\n🌐 آدرس‌های تست:"
echo "1. تست جستجوی کامل: file://$(pwd)/search-test.html"
echo "2. تست سریع: file://$(pwd)/quick-test.html"
echo "3. تست موبایل: file://$(pwd)/mobile-test.html"
echo "4. تست مقاله 203: file://$(pwd)/test-article-203.html"
