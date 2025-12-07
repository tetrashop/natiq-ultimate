#!/usr/bin/env python3
"""
برنامه اصلی natiq-ultimate - نسخه ساده برای شروع
"""

import sys
import os

def main():
    print("🤖 natiq-ultimate - سیستم هوش مصنوعی فارسی")
    print("=" * 50)
    
    # تست کتابخانه‌های اولیه
    print("📦 بررسی کتابخانه‌های ضروری...")
    
    try:
        import transformers
        print(f"✅ transformers نسخه {transformers.__version__}")
    except ImportError as e:
        print(f"❌ transformers: {e}")
        print("\nلطفا نصب کنید: pip install transformers")
        return 1
    
    try:
        import torch
        print(f"✅ torch نسخه {torch.__version__}")
        print(f"   CUDA در دسترس: {torch.cuda.is_available()}")
    except ImportError as e:
        print(f"❌ torch: {e}")
        print("\nلطفا نصب کنید: pip install torch")
        return 1
    
    print("\n✅ محیط آماده است!")
    print("\nبرای تست سیستم، لطفا دستور زیر را اجرا کنید:")
    print("  python src/test_nlp.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
