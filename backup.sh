#!/bin/bash

echo "📦 ایجاد پشتیبان از ناتیق اولتیمیت"
echo "================================"

# ایجاد پوشه پشتیبان
BACKUP_DIR="../natiq-backups"
mkdir -p "$BACKUP_DIR"

# نام فایل پشتیبان
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="natiq-ultimate-backup-$TIMESTAMP.tar.gz"

# ایجاد پشتیبان
echo "🔍 در حال جمع‌آوری فایل‌ها..."
tar --exclude='node_modules' \
    --exclude='.vercel' \
    --exclude='__pycache__' \
    -czf "$BACKUP_DIR/$BACKUP_FILE" .

# نمایش نتیجه
SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)
echo "✅ پشتیبان ایجاد شد:"
echo "   📁 فایل: $BACKUP_FILE"
echo "   📊 حجم: $SIZE"
echo "   📍 مسیر: $BACKUP_DIR/"
echo ""
echo "📋 لیست پشتیبان‌ها:"
ls -lh "$BACKUP_DIR"/natiq-ultimate-backup-*.tar.gz 2>/dev/null || echo "   (هیچ پشتیبانی یافت نشد)"
