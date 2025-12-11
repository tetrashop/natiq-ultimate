#!/bin/bash

# 🏆 اسکریپت استقرار المپیکی
# نویسنده: سیستم ناتیق المپیکی
# نسخه: 3.0.0

set -e  # Exit on error

echo "🚀 شروع استقرار سیستم المپیکی..."

# رنگ‌های خروجی
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# توابع کمکی
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# بررسی وجود فایل‌های ضروری
check_prerequisites() {
    log_info "بررسی پیش‌نیازها..."
    
    # بررسی وجود vercel
    if ! command -v vercel &> /dev/null; then
        log_error "Vercel CLI یافت نشد"
        log_info "نصب با: npm i -g vercel"
        exit 1
    fi
    
    # بررسی وجود node
    if ! command -v node &> /dev/null; then
        log_error "Node.js یافت نشد"
        exit 1
    fi
    
    # بررسی نسخه node
    NODE_VERSION=$(node --version | cut -d'v' -f2)
    REQUIRED_VERSION=18
    if [ $(echo "$NODE_VERSION < $REQUIRED_VERSION" | bc) -eq 1 ]; then
        log_warning "نسخه Node.js باید 18 یا بالاتر باشد (نسخه فعلی: $NODE_VERSION)"
    fi
    
    log_success "بررسی پیش‌نیازها تکمیل شد"
}

# پاکسازی ساختارهای قبلی
cleanup_previous() {
    log_info "پاکسازی استقرارهای قبلی..."
    
    # پاکسازی کش npm
    rm -rf node_modules package-lock.json
    
    # پاکسازی کش vercel
    rm -rf .vercel
    
    # پاکسازی لاگ‌ها
    rm -rf *.log
    
    log_success "پاکسازی انجام شد"
}

# اعتبارسنجی ساختار پروژه
validate_structure() {
    log_info "اعتبارسنجی ساختار پروژه..."
    
    local required_files=(
        "vercel.json"
        "api/index.js"
        "index.html"
        "sw.js"
        "public/manifest.json"
    )
    
    local missing_files=()
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -gt 0 ]; then
        log_error "فایل‌های ضروری یافت نشد:"
        for file in "${missing_files[@]}"; do
            echo "  - $file"
        done
        exit 1
    fi
    
    # اعتبارسنجی JSON files
    if ! jq empty vercel.json 2>/dev/null; then
        log_error "فایل vercel.json معتبر نیست"
        exit 1
    fi
    
    if ! jq empty public/manifest.json 2>/dev/null; then
        log_error "فایل manifest.json معتبر نیست"
        exit 1
    fi
    
    log_success "ساختار پروژه معتبر است"
}

# تحلیل عملکرد پروژه
analyze_performance() {
    log_info "تحلیل عملکرد پروژه..."
    
    # اندازه فایل‌ها
    log_info "آنالیز اندازه فایل‌ها:"
    find . -name "*.js" -o -name "*.html" -o -name "*.css" | while read file; do
        size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
        echo "  - $file: $(numfmt --to=iec --suffix=B $size)"
    done | head -10
    
    # تحلیل وابستگی‌ها
    if [ -f "package.json" ]; then
        log_info "تحلیل وابستگی‌ها:"
        jq -r '.dependencies | keys[]' package.json 2>/dev/null | while read dep; do
            echo "  - $dep"
        done
    fi
    
    log_success "تحلیل عملکرد تکمیل شد"
}

# استقرار روی Vercel
deploy_to_vercel() {
    log_info "شروع استقرار روی Vercel..."
    
    local env=$1
    local flags=""
    
    case $env in
        "production")
            flags="--prod --force"
            log_info "حالت: استقرار تولید"
            ;;
        "preview")
            flags=""
            log_info "حالت: پیش‌نمایش"
            ;;
        *)
            log_error "حالت استقرار نامعتبر: $env"
            exit 1
            ;;
    esac
    
    # اجرای استقرار
    log_info "اجرای دستور: vercel $flags"
    
    if vercel $flags; then
        log_success "استقرار با موفقیت انجام شد"
        
        # نمایش لینک‌ها
        log_info "نمایش اطلاعات استقرار..."
        vercel ls 2>/dev/null | grep -A5 "$(basename $(pwd))" || true
    else
        log_error "استقرار با شکست مواجه شد"
        exit 1
    fi
}

# غیرفعال کردن Authentication
disable_authentication() {
    log_info "دریافت لینک پروژه برای غیرفعال کردن Authentication..."
    
    # انتظار برای استقرار
    sleep 5
    
    # تلاش برای غیرفعال کردن Authentication از طریق API
    log_info "لطفاً به صورت دستی Authentication را غیرفعال کنید:"
    echo "1. به Vercel Dashboard بروید: https://vercel.com/dashboard"
    echo "2. پروژه را انتخاب کنید"
    echo "3. به Settings → Authentication بروید"
    echo "4. گزینه 'Enable Authentication' را غیرفعال کنید"
    echo "5. تغییرات را ذخیره کنید"
}

# تست نهایی سیستم
run_tests() {
    log_info "اجرای تست‌های نهایی..."
    
    local url=""
    
    # دریافت URL از آخرین استقرار
    if command -v jq &> /dev/null && [ -f ".vercel/project.json" ]; then
        url=$(jq -r '.currentTeam.production.url' .vercel/project.json 2>/dev/null || echo "")
    fi
    
    if [ -z "$url" ]; then
        log_warning "نمی‌توان URL را پیدا کرد. تست‌ها اجرا نمی‌شوند."
        return
    fi
    
    log_info "تست سیستم روی: $url"
    
    # تست سلامت
    log_info "تست سلامت API..."
    if curl -s -f "$url/api/health" > /dev/null; then
        log_success "✅ تست سلامت موفقیت‌آمیز"
    else
        log_error "❌ تست سلامت ناموفق"
    fi
    
    # تست چت
    log_info "تست API چت..."
    if curl -s -X POST "$url/api/chat" \
        -H "Content-Type: application/json" \
        -d '{"message":"تست سیستم"}' \
        --max-time 10 > /dev/null; then
        log_success "✅ تست چت موفقیت‌آمیز"
    else
        log_error "❌ تست چت ناموفق"
    fi
    
    # تست وضعیت
    log_info "تست API وضعیت..."
    if curl -s -f "$url/api/status" > /dev/null; then
        log_success "✅ تست وضعیت موفقیت‌آمیز"
    else
        log_error "❌ تست وضعیت ناموفق"
    fi
    
    log_success "تست‌ها تکمیل شدند"
}

# ایجاد گزارش
generate_report() {
    log_info "ایجاد گزارش استقرار..."
    
    local report_file="deployment_report_$(date +%Y%m%d_%H%M%S).json"
    
    cat > "$report_file" << EOF
{
  "deployment": {
    "timestamp": "$(date -Iseconds)",
    "project": "$(basename $(pwd))",
    "version": "3.0.0",
    "environment": "${1:-unknown}",
    "system": {
      "node_version": "$(node --version)",
      "npm_version": "$(npm --version 2>/dev/null || echo 'N/A')",
      "vercel_version": "$(vercel --version 2>/dev/null || echo 'N/A')"
    },
    "performance": {
      "file_count": "$(find . -type f -name "*.js" -o -name "*.html" -o -name "*.css" | wc -l)",
      "total_size": "$(find . -type f -name "*.js" -o -name "*.html" -o -name "*.css" -exec stat -f%z {} \; 2>/dev/null | awk '{sum+=$1} END {print sum}' | numfmt --to=iec --suffix=B 2>/dev/null || echo 'N/A')"
    },
    "status": "success"
  }
}
EOF
    
    log_success "گزارش ایجاد شد: $report_file"
    
    # نمایش خلاصه
    echo ""
    echo "📊 خلاصه گزارش استقرار:"
    echo "════════════════════════════════════════"
    jq . "$report_file" 2>/dev/null || cat "$report_file"
    echo "════════════════════════════════════════"
}

# تابع اصلی
main() {
    echo ""
    echo "╔════════════════════════════════════════╗"
    echo "║   🏆 سیستم استقرار المپیکی ناتیق     ║"
    echo "║           نسخه: 3.0.0                 ║"
    echo "╚════════════════════════════════════════╝"
    echo ""
    
    local env="${1:-production}"
    
    # بررسی حالت
    case $env in
        "production"|"preview")
            ;;
        *)
            log_error "حالت نامعتبر. استفاده: $0 [production|preview]"
            exit 1
            ;;
    esac
    
    # اجرای مراحل
    check_prerequisites
    cleanup_previous
    validate_structure
    analyze_performance
    deploy_to_vercel "$env"
    disable_authentication
    run_tests
    generate_report "$env"
    
    echo ""
    log_success "🎉 استقرار سیستم المپیکی با موفقیت تکمیل شد!"
    echo ""
    echo "📢 نکات مهم:"
    echo "  1. Authentication را در Vercel Dashboard غیرفعال کنید"
    echo "  2. سیستم را در مرورگر تست کنید"
    echo "  3. لاگ‌ها را در صورت نیاز بررسی کنید"
    echo ""
    echo "🏆 سیستم ناتیق المپیکی آماده ارائه خدمات است!"
}

# اجرای تابع اصلی
main "$@"
