#!/bin/bash
echo "🔄 راه‌اندازی پروژه نطق مصطلح برای GitHub..."

# 1. توقف سرورهای قبلی
echo "⏹️  توقف سرورهای قبلی..."
pkill -f "node" 2>/dev/null
sleep 2

# 2. راه‌اندازی سرور
echo "🚀 راه‌اندازی سرور..."
cd ~/natiq-ultimate
node simple-server.cjs > server.log 2>&1 &
sleep 3

# 3. بررسی وضعیت سرور
if curl -s http://localhost:3000/api/health > /dev/null; then
    echo "✅ سرور فعال روی http://localhost:3000"
else
    # تغییر پورت به 3001
    echo "🔄 تغییر پورت به 3001..."
    pkill -f "node"
    sed -i 's/3000/3001/g' simple-server.cjs
    node simple-server.cjs > server.log 2>&1 &
    sleep 3
    echo "✅ سرور فعال روی http://localhost:3001"
fi

# 4. راهنمای GitHub
echo ""
echo "📋 برای آپلود روی GitHub:"
echo "1. به https://github.com/new بروید"
echo "2. نام مخزن: natiq-maslul"
echo "3. Public انتخاب کنید"
echo "4. Initialize with README را تیک نزنید"
echo "5. Create repository را کلیک کنید"
echo ""
echo "6. سپس این دستورات را اجرا کنید:"
echo "   cd ~/natiq-ultimate"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'اولین نسخه'"
echo "   git remote add origin https://github.com/tetrashop/natiq-maslul.git"
echo "   git branch -M main"
echo "   git push -u origin main"
