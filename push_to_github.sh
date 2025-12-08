#!/bin/bash
# اسکریپت امن برای آپلود natiq-ultimate به GitHub

echo "🔐 شروع فرآیند آپلود امن..."

# 1. تنظیم اطلاعات کاربر
read -p "لطفاً نام کاربری GitHub خود را وارد کنید: " GITHUB_USERNAME
read -p "آیا از آدرس 'https://github.com/${GITHUB_USERNAME}/natiq-ultimate.git' مطمئن هستید؟ (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ عملیات لغو شد."
    exit 1
fi

# 2. حذف فایل‌های حساس
echo "🗑️  حذف فایل‌های حساس از Git..."
git rm --cached .env .env.local 2>/dev/null || true
git rm --cached *.log 2>/dev/null || true
git rm --cached natiq-offline-bundle.tar.gz 2>/dev/null || true

# 3. به‌روزرسانی gitignore
echo "📝 به‌روزرسانی .gitignore..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# فایل‌های حساس پروژه
.env
.env.local
.env.*
!.env.example
config.json
credentials.json
secrets/
keys/
*.pem
*.key
*.crt

# لاگ‌ها
*.log
logs/
monitor.log
error.log
server-*.log
natiq.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Vercel
.vercel

# فایل‌های موقت
*.tmp
*.temp
*~

# آرشیوهای بزرگ
*.tar.gz
*.zip
*.rar

# پکیج‌های آفلاین
offline_packages/
natiq-offline-bundle.tar.gz

# پشتیبان‌گیری
backup_*/
backups/
*.bak

# Termux-specific
termux/

# فایل‌های اشتباه
earch*
tall*
'earch*'
'tall*'
