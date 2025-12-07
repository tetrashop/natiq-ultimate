#!/bin/bash
# اسکریپت راه‌اندازی natiq-ultimate

echo "🚀 راه‌اندازی natiq-ultimate v2.0"
echo "================================"

# رنگ‌ها
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# توابع کمکی
log_info() { echo -e "${GREEN}✅ $1${NC}"; }
log_warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# بررسی پایتون
if ! command -v python3 &> /dev/null; then
    log_error "پایتون یافت نشد!"
    exit 1
fi

log_info "پایتون: $(python3 --version)"

# بررسی نیازمندی‌ها
cd backend
if [ -f "requirements.txt" ]; then
    log_info "نصب نیازمندی‌ها..."
    pip install -r requirements.txt
else
    log_warn "فایل requirements.txt یافت نشد"
fi

# ایجاد پوشه‌های ضروری
mkdir -p ../data/knowledge ../data/conversations ../data/models

# راه‌اندازی سرور
log_info "راه‌اندازی سرور..."
echo ""
echo "🌐 سرور در حال اجرا است:"
echo "   📍 آدرس: http://localhost:8000"
echo "   📍 آدرس شبکه: http://$(hostname -I | awk '{print $1}'):8000"
echo "   📱 واسط کاربری: http://localhost:8000"
echo ""
echo "برای توقف: Ctrl+C"
echo "================================"

# اجرای سرور
python3 server.py
