#!/bin/bash

echo "🔐 آپلود به GitHub با SSH"
echo "========================"

# بررسی وجود SSH key
if [ ! -f ~/.ssh/id_rsa.pub ]; then
    echo "🔑 ایجاد SSH Key..."
    ssh-keygen -t rsa -b 4096 -C "natiq-ultimate@github" -f ~/.ssh/id_rsa -N ""
    echo "✅ SSH Key ایجاد شد"
    echo ""
    echo "📋 کلید عمومی شما:"
    cat ~/.ssh/id_rsa.pub
    echo ""
    echo "لطفا این کلید را به GitHub اضافه کنید:"
    echo "1. به https://github.com/settings/keys بروید"
    echo "2. روی 'New SSH key' کلیک کنید"
    echo "3. کلید بالا را کپی کنید"
    read -p "پس از اضافه کردن کلید، Enter بزنید..." 
fi

# اطلاعات ریپازیتوری
read -p "GitHub Username: " USERNAME
read -p "Repository Name: " REPO_NAME

# تنظیم remote با SSH
git remote remove origin 2>/dev/null
git remote add origin git@github.com:$USERNAME/$REPO_NAME.git

# پوش کردن
echo "📤 در حال آپلود..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ آپلود موفق!"
    echo "🌐 آدرس: https://github.com/$USERNAME/$REPO_NAME"
else
    echo "❌ خطا در آپلود"
    echo "ممکن است نیاز باشد ابتدا ریپازیتوری را در GitHub بسازید."
    echo "به https://github.com/new بروید و ریپازیتوری '$REPO_NAME' را ایجاد کنید."
fi
