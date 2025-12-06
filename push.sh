#!/bin/bash

# رنگ‌ها برای نمایش بهتر
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 آپلود پروژه نطق مصطلح به GitHub${NC}"
echo "=========================================="

# بررسی وضعیت Git
cd ~/natiq-ultimate

echo -e "${YELLOW}📊 بررسی وضعیت فعلی...${NC}"
git status

# اضافه کردن تغییرات
echo -e "\n${YELLOW}📁 اضافه کردن تغییرات...${NC}"
git add .

# Commit
if [ -n "$1" ]; then
    COMMIT_MSG="$1"
else
    COMMIT_MSG="به‌روزرسانی پروژه نطق مصطلح - $(date '+%Y-%m-%d %H:%M:%S')"
fi

echo -e "\n${YELLOW}💾 ثبت تغییرات با پیام:${NC}"
echo -e "   \"$COMMIT_MSG\""
git commit -m "$COMMIT_MSG"

# آپلود به GitHub
echo -e "\n${YELLOW}📤 آپلود به GitHub...${NC}"
echo -e "${RED}⚠️  توجه: اگر از توکن استفاده می‌کنی:${NC}"
echo -e "   1. نام کاربری: tetrashop"
echo -e "   2. رمز: توکن GitHub خودت را وارد کن"
echo -e "   (اگر 2FA فعالی، از Settings → Developer settings → Tokens بساز)"
echo ""

# Push
if git push origin main; then
    echo -e "\n${GREEN}✅ آپلود موفق!${NC}"
    echo -e "🌐 پروژه در: ${GREEN}https://github.com/tetrashop/natiq-ultimate${NC}"
    
    # نمایش آخرین commit
    echo -e "\n📝 آخرین commit:"
    git log --oneline -1
    
    # آمار
    echo -e "\n📊 آمار پروژه:"
    echo "   مقالات: 199 مقاله NLP فارسی"
    echo "   سرور: http://localhost:3000"
    echo "   API: سلامت و جستجو فعال"
else
    echo -e "\n${RED}❌ خطا در آپلود!${NC}"
    echo "مشکلات احتمالی:"
    echo "   1. اتصال اینترنت"
    echo "   2. توکن GitHub منقضی شده"
    echo "   3. Conflict با تغییرات دیگران"
    echo ""
    echo "راه‌حل:"
    echo "   git pull origin main --rebase"
    echo "   سپس دوباره push.sh اجرا کن"
fi
