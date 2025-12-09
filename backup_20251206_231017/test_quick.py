#!/usr/bin/env python3
"""
تست سریع عملکرد سیستم
"""

import sys
import os

print("🧪 تست سریع natiq-ultimate")
print("=" * 40)

# بررسی کتابخانه‌های اصلی
libs = [
    ('numpy', 'محاسبات عددی'),
    ('torch', 'هوش مصنوعی'),
    ('transformers', 'پردازش زبان'),
    ('sentencepiece', 'توکنایزر'),
    ('accelerate', 'شتاب‌دهنده')
]

print("📦 بررسی کتابخانه‌ها:")
for lib, desc in libs:
    try:
        __import__(lib)
        version = getattr(sys.modules[lib], '__version__', '?')
        print(f"  ✅ {lib:20} {version:10} ({desc})")
    except ImportError:
        print(f"  ❌ {lib:20} {'NOT FOUND':10} ({desc})")

print("\n📁 بررسی ساختار پروژه:")
paths = [
    ('src/', 'کد منبع'),
    ('models/', 'مدل‌ها'),
    ('data/', 'داده‌ها'),
    ('logs/', 'لاگ‌ها'),
    ('src/main.py', 'فایل اصلی'),
    ('src/config.py', 'تنظیمات'),
]

for path, desc in paths:
    if os.path.exists(path):
        size = os.path.getsize(path) if os.path.isfile(path) else '-'
        print(f"  ✅ {path:20} {str(size):10} ({desc})")
    else:
        print(f"  ❌ {path:20} {'MISSING':10} ({desc})")

print("\n🧠 تست PyTorch:")
try:
    import torch
    print(f"  نسخه: {torch.__version__}")
    print(f"  CUDA در دسترس: {torch.cuda.is_available()}")
    print(f"  تعداد هسته‌ها: {torch.get_num_threads()}")
    
    # تست تانسور ساده
    x = torch.tensor([1.0, 2.0, 3.0])
    print(f"  تست تانسور: {x.sum().item()}")
    
except Exception as e:
    print(f"  ❌ خطا: {e}")

print("\n" + "=" * 40)
print("📋 خلاصه:")
print("  1. فایل setup.sh را برای نصب کامل اجرا کنید")
print("  2. python src/main.py را برای اجرای برنامه")
print("  3. python test_quick.py را برای بررسی سلامت")
print("=" * 40)
