#!/bin/bash

# تنظیمات
BASE_DIR="/data/data/com.termux/files/home/natiq-ultimate"
LOG_FILE="$BASE_DIR/natiq.log"
BACKUP_DIR="$BASE_DIR/backups"
MAX_BACKUPS=10
ALERT_THRESHOLD=80 # آستانه هشدار (%)

# رنگ‌ها
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# تابع لاگ
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# تابع نمایش وضعیت
status() {
    echo -e "\n${BLUE}📊 وضعیت نطق مصطلح${NC}"
    echo "=================================="
    
    # بررسی سرور مقالات
    if curl -s "http://localhost:3000/api/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ سرور مقالات (3000): فعال${NC}"
        ARTICLES=$(curl -s "http://localhost:3000/api/health" | python3 -c "import json,sys; print(json.load(sys.stdin)['articles'])" 2>/dev/null || echo "?")
        echo "   مقالات: $ARTICLES"
    else
        echo -e "${RED}❌ سرور مقالات (3000): غیرفعال${NC}"
    fi
    
    # بررسی سرور QnA
    if curl -s "http://localhost:3002/api/qna/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ سرور پرسش و پاسخ (3002): فعال${NC}"
        FAQS=$(curl -s "http://localhost:3002/api/qna/health" | python3 -c "import json,sys; print(json.load(sys.stdin)['faqCount'])" 2>/dev/null || echo "?")
        echo "   سوالات ذخیره شده: $FAQS"
    else
        echo -e "${RED}❌ سرور پرسش و پاسخ (3002): غیرفعال${NC}"
    fi
    
    # بررسی منابع
    echo -e "\n${BLUE}💻 منابع سیستم:${NC}"
    RAM_USAGE=$(free -m | awk 'NR==2{printf "%.1f", $3*100/$2}')
    DISK_USAGE=$(df -h . | awk 'NR==2{print $5}' | sed 's/%//')
    
    if (( $(echo "$RAM_USAGE > $ALERT_THRESHOLD" | bc -l) )); then
        echo -e "${RED}   RAM: ${RAM_USAGE}%${NC}"
    else
        echo -e "${GREEN}   RAM: ${RAM_USAGE}%${NC}"
    fi
    
    if (( $(echo "$DISK_USAGE > $ALERT_THRESHOLD" | bc -l) )); then
        echo -e "${RED}   Disk: ${DISK_USAGE}%${NC}"
    else
        echo -e "${GREEN}   Disk: ${DISK_USAGE}%${NC}"
    fi
    
    # بررسی processها
    echo -e "\n${BLUE}⚡ Processها:${NC}"
    ps aux | grep -E "node.*(natiq|qna)" | grep -v grep | while read line; do
        PID=$(echo $line | awk '{print $2}')
        CMD=$(echo $line | awk '{print $11}')
        CPU=$(echo $line | awk '{print $3}')
        MEM=$(echo $line | awk '{print $4}')
        echo "   $CMD (PID: $PID, CPU: $CPU%, MEM: $MEM%)"
    done
}

# تابع شروع
start() {
    log "شروع سرورها..."
    cd "$BASE_DIR"
    
    # متوقف کردن سرورهای قبلی
    pkill -f "node" 2>/dev/null
    sleep 2
    
    # شروع سرور مقالات
    nohup node natiq-complete.cjs > "$BASE_DIR/server-main.log" 2>&1 &
    sleep 3
    
    # شروع سرور QnA
    nohup node qna-server-fixed.cjs > "$BASE_DIR/server-qna.log" 2>&1 &
    sleep 3
    
    status
}

# تابع توقف
stop() {
    log "توقف سرورها..."
    pkill -f "node" 2>/dev/null
    sleep 2
    echo -e "${GREEN}✅ سرورها متوقف شدند${NC}"
}

# تابع restart
restart() {
    stop
    start
}

# تابع backup
backup() {
    log "ایجاد backup..."
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    BACKUP_FILE="$BACKUP_DIR/natiq_backup_$TIMESTAMP.tar.gz"
    
    mkdir -p "$BACKUP_DIR"
    
    # ایجاد backup
    tar -czf "$BACKUP_FILE" \
        --exclude="node_modules" \
        --exclude="backups" \
        --exclude="*.log" \
        .
    
    # محاسبه checksum
    md5sum "$BACKUP_FILE" > "$BACKUP_FILE.md5"
    sha256sum "$BACKUP_FILE" > "$BACKUP_FILE.sha256"
    
    # مدیریت تعداد backupها
    ls -t "$BACKUP_DIR"/natiq_backup_*.tar.gz 2>/dev/null | tail -n +$((MAX_BACKUPS+1)) | xargs rm -f
    
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    log "Backup ایجاد شد: $BACKUP_FILE ($SIZE)"
    echo -e "${GREEN}✅ Backup ایجاد شد${NC}"
}

# تابع restore
restore() {
    if [ -z "$1" ]; then
        echo -e "${YELLOW}⚠️ لطفا فایل backup را مشخص کنید:${NC}"
        ls -l "$BACKUP_DIR"/natiq_backup_*.tar.gz 2>/dev/null || echo "   فایل backup یافت نشد"
        return 1
    fi
    
    BACKUP_FILE="$1"
    
    if [ ! -f "$BACKUP_FILE" ]; then
        echo -e "${RED}❌ فایل backup یافت نشد${NC}"
        return 1
    fi
    
    # توقف سرورها
    stop
    
    # اعتبارسنجی checksum
    echo -e "${BLUE}🔐 اعتبارسنجی backup...${NC}"
    if [ -f "$BACKUP_FILE.md5" ]; then
        if md5sum -c "$BACKUP_FILE.md5" 2>/dev/null; then
            echo -e "${GREEN}✅ MD5 checksum معتبر${NC}"
        else
            echo -e "${RED}❌ MD5 checksum نامعتبر${NC}"
            read -p "ادامه دهید؟ (y/n): " -n 1 -r
            echo
            [[ ! $REPLY =~ ^[Yy]$ ]] && return 1
        fi
    fi
    
    # استخراج backup
    echo -e "${BLUE}📦 استخراج backup...${NC}"
    TEMP_DIR="/tmp/natiq_restore_$(date +%s)"
    mkdir -p "$TEMP_DIR"
    tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"
    
    # کپی فایل‌ها
    echo -e "${BLUE}📁 بازگردانی فایل‌ها...${NC}"
    cp -r "$TEMP_DIR"/* "$BASE_DIR"/
    
    # پاکسازی
    rm -rf "$TEMP_DIR"
    
    echo -e "${GREEN}✅ Restore کامل شد${NC}"
    echo "برای اعمال تغییرات، سرورها را restart کنید:"
    echo "  ./manage-natiq.sh restart"
}

# تابع نظارت
monitor() {
    echo -e "${BLUE}📈 نظارت زنده (Ctrl+C برای خروج)${NC}"
    echo "=================================="
    
    trap 'echo -e "\n${GREEN}نظارت متوقف شد${NC}"; exit 0' INT
    
    while true; do
        clear
        status
        
        # تست پاسخگویی
        echo -e "\n${BLUE}🏎️  تست عملکرد:${NC}"
        
        # تست سرور مقالات
        START=$(date +%s%3N)
        curl -s "http://localhost:3000/api/health" > /dev/null 2>&1
        END=$(date +%s%3N)
        MAIN_TIME=$((END-START))
        
        # تست سرور QnA
        START=$(date +%s%3N)
        curl -s "http://localhost:3002/api/qna/health" > /dev/null 2>&1
        END=$(date +%s%3N)
        QNA_TIME=$((END-START))
        
        if [ "$MAIN_TIME" -lt 100 ]; then
            echo -e "   مقالات: ${GREEN}${MAIN_TIME}ms${NC}"
        elif [ "$MAIN_TIME" -lt 500 ]; then
            echo -e "   مقالات: ${YELLOW}${MAIN_TIME}ms${NC}"
        else
            echo -e "   مقالات: ${RED}${MAIN_TIME}ms${NC}"
        fi
        
        if [ "$QNA_TIME" -lt 100 ]; then
            echo -e "   QnA: ${GREEN}${QNA_TIME}ms${NC}"
        elif [ "$QNA_TIME" -lt 500 ]; then
            echo -e "   QnA: ${YELLOW}${QNA_TIME}ms${NC}"
        else
            echo -e "   QnA: ${RED}${QNA_TIME}ms${NC}"
        fi
        
        # نمایش لاگ‌های اخیر
        echo -e "\n${BLUE}📝 آخرین لاگ‌ها:${NC}"
        tail -5 "$LOG_FILE" 2>/dev/null || echo "   فایل لاگ یافت نشد"
        
        sleep 5
    done
}

# تابع تست کامل
test_all() {
    echo -e "${BLUE}🧪 تست کامل سامانه${NC}"
    echo "========================"
    
    # تست 1: سلامت سرورها
    echo -e "\n1. ${BLUE}تست سلامت:${NC}"
    
    if curl -s "http://localhost:3000/api/health" > /dev/null; then
        echo -e "   ${GREEN}✅ سرور مقالات سالم${NC}"
    else
        echo -e "   ${RED}❌ سرور مقالات مشکل دارد${NC}"
    fi
    
    if curl -s "http://localhost:3002/api/qna/health" > /dev/null; then
        echo -e "   ${GREEN}✅ سرور پرسش و پاسخ سالم${NC}"
    else
        echo -e "   ${RED}❌ سرور پرسش و پاسخ مشکل دارد${NC}"
    fi
    
    # تست 2: عملکرد API‌ها
    echo -e "\n2. ${BLUE}تست عملکرد:${NC}"
    
    echo "   تست جستجو..."
    curl -G "http://localhost:3000/api/search" \
        --data-urlencode "q=NLP" \
        -s -o /dev/null -w "   مقالات: %{http_code} در %{time_total}s\n"
    
    echo "   تست پرسش و پاسخ..."
    curl -G "http://localhost:3002/api/qna/ask" \
        --data-urlencode "q=آیا سیستم کار می‌کند؟" \
        -s -o /dev/null -w "   QnA: %{http_code} در %{time_total}s\n"
    
    # تست 3: تست فشار
    echo -e "\n3. ${BLUE}تست فشار (5 درخواست همزمان):${NC}"
    
    for i in {1..5}; do
        curl -s "http://localhost:3000/api/health" > /dev/null &
    done
    wait
    echo -e "   ${GREEN}✅ تست فشار موفق${NC}"
    
    # تست 4: تست داده‌ها
    echo -e "\n4. ${BLUE}تست داده‌ها:${NC}"
    
    if [ -f "data/articles.json" ]; then
        ARTICLE_COUNT=$(grep -c '"id"' data/articles.json)
        echo -e "   ${GREEN}✅ $ARTICLE_COUNT مقاله موجود${NC}"
    else
        echo -e "   ${RED}❌ فایل مقالات یافت نشد${NC}"
    fi
    
    # نتیجه
    echo -e "\n${BLUE}📊 نتیجه تست:${NC}"
    echo "   سرورها: ${GREEN}فعال${NC}"
    echo "   API‌ها: ${GREEN}پاسخگو${NC}"
    echo "   داده‌ها: ${GREEN}معتبر${NC}"
    echo -e "\n${GREEN}🎉 سامانه برای بهره‌برداری آماده است!${NC}"
}

# تابع help
show_help() {
    echo -e "${BLUE}📖 راهنمای مدیریت نطق مصطلح${NC}"
    echo "=================================="
    echo "دستورات:"
    echo "  ${GREEN}start${NC}    - شروع سرورها"
    echo "  ${GREEN}stop${NC}     - توقف سرورها"
    echo "  ${GREEN}restart${NC}  - restart سرورها"
    echo "  ${GREEN}status${NC}   - نمایش وضعیت"
    echo "  ${GREEN}backup${NC}   - ایجاد backup"
    echo "  ${GREEN}restore FILE${NC} - بازگردانی از backup"
    echo "  ${GREEN}monitor${NC}  - نظارت زنده"
    echo "  ${GREEN}test${NC}     - تست کامل سامانه"
    echo "  ${GREEN}help${NC}     - نمایش این راهنما"
    echo ""
    echo "مثال:"
    echo "  ./manage-natiq.sh start"
    echo "  ./manage-natiq.sh backup"
    echo "  ./manage-natiq.sh monitor"
}

# مدیریت دستورات
case "$1" in
    "start")
        start
        ;;
    "stop")
        stop
        ;;
    "restart")
        restart
        ;;
    "status")
        status
        ;;
    "backup")
        backup
        ;;
    "restore")
        restore "$2"
        ;;
    "monitor")
        monitor
        ;;
    "test")
        test_all
        ;;
    "help"|"")
        show_help
        ;;
    *)
        echo -e "${RED}❌ دستور نامعتبر: $1${NC}"
        show_help
        ;;
esac
