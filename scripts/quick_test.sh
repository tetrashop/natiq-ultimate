#!/bin/bash
# تست سریع natiq-ultimate

echo "🚀 شروع تست سریع natiq-ultimate"
echo "================================"

# رنگ‌ها
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# تابع تست
test_endpoint() {
    local url=$1
    local name=$2
    
    echo -n "🔍 تست $name... "
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" --max-time 5)
    
    if [ "$response" = "200" ] || [ "$response" = "201" ]; then
        echo -e "${GREEN}✅ موفق ($response)${NC}"
        return 0
    else
        echo -e "${RED}❌ خطا ($response)${NC}"
        return 1
    fi
}

# 1. تست سلامت سرور
echo -e "\n${BLUE}1. تست سلامت سرور:${NC}"
test_endpoint "http://localhost:8000/api/health" "وضعیت سرور"

# 2. تست صفحه اصلی
echo -e "\n${BLUE}2. تست صفحات وب:${NC}"
test_endpoint "http://localhost:8000/" "صفحه اصلی"

# 3. تست API چت
echo -e "\n${BLUE}3. تست API چت:${NC}"
SESSION_ID="test_$(date +%s)"
RESPONSE=$(curl -s -X POST "http://localhost:8000/api/chat/$SESSION_ID" \
    -H "Content-Type: application/json" \
    -d '{"message":"سلام"}' \
    --max-time 10)

if echo "$RESPONSE" | grep -q "answer"; then
    echo -e "${GREEN}✅ API چت کار می‌کند${NC}"
    ANSWER=$(echo "$RESPONSE" | grep -o '"answer":"[^"]*' | cut -d'"' -f4)
    echo "   پاسخ: ${ANSWER:0:50}..."
else
    echo -e "${RED}❌ API چت پاسخ نداد${NC}"
    echo "   پاسخ خام: $RESPONSE"
fi

# 4. تست فایل‌های استاتیک
echo -e "\n${BLUE}4. تست فایل‌های استاتیک:${NC}"
test_endpoint "http://localhost:8000/static/css/style.css" "فایل CSS"
test_endpoint "http://localhost:8000/static/js/app.js" "فایل JavaScript"

# 5. بررسی فرآیند سرور
echo -e "\n${BLUE}5. بررسی فرآیند سرور:${NC}"
if pgrep -f "python.*server.py" > /dev/null; then
    echo -e "${GREEN}✅ سرور FastAPI در حال اجراست${NC}"
else
    echo -e "${RED}❌ سرور FastAPI اجرا نیست${NC}"
    echo "   دستور راه‌اندازی: ./scripts/start.sh"
fi

# 6. تست دستی رابط کاربری
echo -e "\n${BLUE}6. راهنمای تست رابط کاربری:${NC}"
echo -e "${YELLOW}📱 مراحل تست دستی:${NC}"
echo "   1. مرورگر را باز کنید"
echo "   2. به آدرس http://localhost:8000 بروید"
echo "   3. روی دکمه '💬 شروع چت' کلیک کنید"
echo "   4. یک پیام ارسال کنید"
echo "   5. پاسخ ربات را بررسی کنید"
echo "   6. از پنل کناری برای تست اتصال استفاده کنید"

echo -e "\n${GREEN}✨ تست سریع کامل شد!${NC}"
echo -e "${YELLOW}💡 نکته: برای تست کامل‌تر، اسکریپت Python را اجرا کنید:${NC}"
echo "   python scripts/test_system.py"
