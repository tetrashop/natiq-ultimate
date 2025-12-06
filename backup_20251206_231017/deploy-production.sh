#!/bin/bash

echo "🚀 استقرار نطق مصطلح در محیط production"
echo "====================================="

# 1. بررسی pre-requisites
echo -e "\n1. 🔍 بررسی پیش‌نیازها:"

# بررسی Node.js
if ! command -v node &> /dev/null; then
    echo "   ❌ Node.js نصب نیست"
    exit 1
else
    echo "   ✅ Node.js نصب است: $(node --version)"
fi

# بررسی npm
if ! command -v npm &> /dev/null; then
    echo "   ⚠️ npm نصب نیست"
else
    echo "   ✅ npm نصب است: $(npm --version)"
fi

# بررسی پورت‌ها
echo -e "\n2. 🔌 بررسی پورت‌ها:"

for port in 3000 3002; do
    if lsof -i :$port > /dev/null 2>&1; then
        echo "   ⚠️ پورت $port در حال استفاده است"
        read -p "   آیا می‌خواهید آن را آزاد کنید؟ (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            fuser -k $port/tcp 2>/dev/null
            echo "   ✅ پورت $port آزاد شد"
        fi
    else
        echo "   ✅ پورت $port آزاد است"
    fi
done

# 3. نصب وابستگی‌ها
echo -e "\n3. 📦 نصب وابستگی‌ها:"

if [ -f "package.json" ]; then
    echo "   نصب packages..."
    npm install --production 2>&1 | tail -5
    echo "   ✅ وابستگی‌ها نصب شدند"
else
    echo "   ⚠️ package.json یافت نشد"
fi

# 4. تنظیمات محیط
echo -e "\n4. ⚙️  تنظیمات محیط:"

# ایجاد دایرکتوری لاگ
mkdir -p logs
echo "   ✅ دایرکتوری logs ایجاد شد"

# ایجاد دایرکتوری backup
mkdir -p backups
echo "   ✅ دایرکتوری backups ایجاد شد"

# تنظیم permission
chmod 755 *.sh
chmod 644 *.js *.cjs *.json
echo "   ✅ permission تنظیم شد"

# 5. ایجاد service برای auto-start
echo -e "\n5. 🎯 ایجاد سرویس خودکار:"

cat > /etc/systemd/system/natiq.service 2>/dev/null || cat > natiq-service.sh << 'SERVICE'
#!/bin/bash
cd /data/data/com.termux/files/home/natiq-ultimate
node natiq-complete.cjs &
node qna-server-fixed.cjs &
SERVICE

if [ -f "natiq-service.sh" ]; then
    chmod +x natiq-service.sh
    echo "   ✅ اسکریپت سرویس ایجاد شد"
fi

# 6. راه‌اندازی
echo -e "\n6. 🚀 راه‌اندازی سامانه:"

./manage-natiq.sh stop
sleep 2
./manage-natiq.sh start
sleep 3

# 7. تست نهایی
echo -e "\n7. 🧪 تست نهایی استقرار:"

./manage-natiq.sh test

# 8. نمایش اطلاعات
echo -e "\n📋 اطلاعات استقرار:"
echo "   آدرس API مقالات: http://localhost:3000"
echo "   آدرس API پرسش و پاسخ: http://localhost:3002"
echo "   تست رابط کاربری: file://$(pwd)/test-qna-fixed.html"
echo "   مدیریت سامانه: ./manage-natiq.sh"
echo -e "\n🔒 نکات امنیتی:"
echo "   1. فایل‌های backup را در محل امن نگهداری کنید"
echo "   2. regular backup از داده‌ها بگیرید"
echo "   3. monitor وضعیت سامانه"
echo "   4. از اسکریپت optimize-system.sh برای نگهداری استفاده کنید"

echo -e "\n🎉 استقرار با موفقیت انجام شد!"
