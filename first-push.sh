#!/bin/bash
echo "📦 آپلود اولیه پروژه به GitHub"
cd ~/natiq-ultimate

# تنظیمات اولیه (فقط بار اول)
git init
git add .
git commit -m "پروژه نهایی نطق مصطلح - سیستم جستجوی مقالات NLP فارسی"

# اتصال به GitHub
git remote add origin https://github.com/tetrashop/natiq-ultimate.git
git branch -M main

# آپلود
echo "🔐 وارد کردن اطلاعات GitHub:"
echo "Username: tetrashop"
echo "Password: از توکن GitHub استفاده کن"
git push -u origin main

echo "✅ انجام شد! آدرس: https://github.com/tetrashop/natiq-ultimate"
