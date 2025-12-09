#!/bin/bash
# اسکریپت راه‌اندازی خودکار natiq-ultimate در Termux

set -e  # در صورت خطا توقف کن

echo "🚀 شروع راه‌اندازی natiq-ultimate"
echo "======================================"

# بررسی وجود پایتون
if ! command -v python3 &> /dev/null; then
    echo "❌ پایتون یافت نشد. در حال نصب..."
    pkg install python -y
fi

# به‌روزرسانی pip
echo "🔧 به‌روزرسانی pip..."
python3 -m pip install --upgrade pip

# نصب PyTorch برای Termux (مخصوص معماری aarch64)
echo "🧠 نصب PyTorch برای Termux..."
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu

# نصب سایر نیازمندی‌ها
echo "📦 نصب نیازمندی‌های پایتون..."
pip install -r requirements_termux.txt

# ایجاد ساختار پوشه‌ها
echo "📁 ایجاد ساختار پوشه‌ها..."
mkdir -p models data logs

# دانلود مدل اولیه (اگر اینترنت وجود دارد)
read -p "آیا می‌خواهید مدل فارسی را دانلود کنید؟ (بله/خیر) " -n 1 -r
echo
if [[ $REPLY =~ ^[بب]$ ]]; then
    echo "📥 در حال دانلود مدل فارسی..."
    python3 << 'END'
from transformers import AutoTokenizer, AutoModel
import os

model_name = "HooshvareLab/bert-base-parsbert-uncased"
save_path = "./models/fa-bert"

print(f"دانلود مدل: {model_name}")
print(f"ذخیره در: {save_path}")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# ذخیره محلی
tokenizer.save_pretrained(save_path)
model.save_pretrained(save_path)
print("✅ مدل با موفقیت دانلود و ذخیره شد")
END
fi

# تست محیط
echo "🧪 تست محیط اجرا..."
python3 -c "
import sys
print(f'پایتون {sys.version}')

try:
    import torch
    print(f'✅ PyTorch {torch.__version__}')
except ImportError as e:
    print(f'❌ PyTorch: {e}')

try:
    import transformers
    print(f'✅ Transformers {transformers.__version__}')
except ImportError as e:
    print(f'❌ Transformers: {e}')
"

# تنظیم مجوزهای اجرا
chmod +x src/main.py

echo ""
echo "======================================"
echo "✅ راه‌اندازی کامل شد!"
echo ""
echo "دستورات اجرا:"
echo "  cd ~/natiq-ultimate"
echo "  python src/main.py"
echo ""
echo "برای تست سریع:"
echo "  python -c \"from src.core.nlp_processor import NLPProcessor; p = NLPProcessor(); print(p.process('سلام'))\""
echo ""
