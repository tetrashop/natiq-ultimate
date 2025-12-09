#!/bin/bash

echo "🛠️  بهینه‌سازی سامانه نطق مصطلح"
echo "=============================="

# 1. بهینه‌سازی حافظه
echo -e "\n1. 🧹 بهینه‌سازی حافظه:"
sync && echo 3 > /proc/sys/vm/drop_caches 2>/dev/null && echo "   ✅ حافظه کش پاک شد"

# 2. بررسی و تعمیر فایل‌ها
echo -e "\n2. 🔧 بررسی یکپارچگی فایل‌ها:"

# بررسی فایل مقالات
if [ -f "data/articles.json" ]; then
    if jq empty data/articles.json 2>/dev/null; then
        echo "   ✅ فایل articles.json معتبر است"
    else
        echo "   ⚠️ فایل articles.json مشکل دارد، در حال تعمیر..."
        cp data/articles.json data/articles.json.bak
        jq . data/articles.json.bak > data/articles.json 2>/dev/null && echo "   ✅ تعمیر شد"
    fi
fi

# 3. بهینه‌سازی الگوریتم‌ها
echo -e "\n3. 🧠 بهینه‌سازی الگوریتم‌ها:"

# ایجاد index برای مقالات
if [ -f "data/articles.json" ]; then
    echo "   ایجاد index برای جستجوی سریعتر..."
    python3 -c "
import json, os, sys
sys.path.append('.')
try:
    with open('data/articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    # ایجاد فایل index
    index = {}
    for i, article in enumerate(articles):
        words = (article.get('title', '') + ' ' + article.get('excerpt', '')).lower().split()
        for word in words:
            if len(word) > 2:
                if word not in index:
                    index[word] = []
                index[word].append(i)
    
    with open('data/search_index.json', 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False)
    
    print('   ✅ Index ایجاد شد: {} کلمه کلیدی'.format(len(index)))
except Exception as e:
    print(f'   ❌ خطا: {e}')
"
fi

# 4. فشرده‌سازی لاگ‌ها
echo -e "\n4. 📦 فشرده‌سازی لاگ‌های قدیمی:"
find . -name "*.log" -size +1M -exec gzip {} \; 2>/dev/null
echo "   ✅ لاگ‌های بزرگ فشرده شدند"

# 5. حذف فایل‌های موقت
echo -e "\n5. 🗑️  پاکسازی فایل‌های موقت:"
find /tmp -name "*natiq*" -type f -mtime +1 -delete 2>/dev/null
find . -name "*.tmp" -delete 2>/dev/null
find . -name "*.bak" -mtime +7 -delete 2>/dev/null
echo "   ✅ فایل‌های موقت پاک شدند"

# 6. بروزرسانی سیستم
echo -e "\n6. 🔄 بررسی بروزرسانی‌ها:"

# بررسی نسخه Node.js
NODE_VERSION=$(node --version 2>/dev/null || echo "v0.0.0")
echo "   Node.js: $NODE_VERSION"

# بررسی وابستگی‌ها
if [ -f "package.json" ]; then
    echo "   📦 بررسی package.json..."
    npm audit 2>/dev/null || echo "   ⚠️ npm audit در دسترس نیست"
fi

# 7. تست نهایی
echo -e "\n7. 🧪 تست نهایی بهینه‌سازی:"

# تست سرعت
echo "   تست سرعت پاسخگویی..."
time curl -s "http://localhost:3000/api/health" > /dev/null 2>&1

# تست حافظه
echo -e "\n   وضعیت حافظه:"
free -m | awk 'NR==2{printf "      استفاده: %sMB از %sMB\n", $3, $2}'

echo -e "\n✅ بهینه‌سازی کامل شد!"
echo "📊 برای نظارت از دستور زیر استفاده کنید:"
echo "   ./manage-natiq.sh monitor"
