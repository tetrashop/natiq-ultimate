#!/usr/bin/env python3
"""
تست بسیار ساده بدون نیاز به PyTorch سنگین
"""

import sys
import os

def test_with_simple_model():
    """استفاده از مدل‌های سبک"""
    print("🧪 تست با مدل‌های سبک")
    print("=" * 50)
    
    try:
        # استفاده از tensorflow به جای torch
        import tensorflow as tf
        print(f"✅ TensorFlow نسخه {tf.__version__}")
        
        # تست یک مدل ساده
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(10, activation='relu'),
            tf.keras.layers.Dense(1)
        ])
        print("✅ مدل TensorFlow ایجاد شد")
        
        return True
    except ImportError:
        print("❌ TensorFlow نیز نصب نیست")
        
        # راه‌حل جایگزین: استفاده از transformers با backend متفاوت
        try:
            os.environ['TRANSFORMERS_BACKEND'] = 'tensorflow'
            from transformers import pipeline
            
            print("🎯 استفاده از transformers با TensorFlow backend")
            return True
        except:
            print("❌ هیچ backend مناسب یافت نشد")
            return False

def install_requirements():
    """نصب نیازمندی‌های سبک"""
    print("\n📦 نصب نیازمندی‌های سبک...")
    
    # لیست پکیج‌های سبک‌تر
    light_packages = [
        'numpy',
        'scipy',
        'sentencepiece',
        'protobuf',
        'tokenizers',
        'accelerate'
    ]
    
    for package in light_packages:
        try:
            __import__(package)
            print(f"  ✅ {package} از قبل نصب است")
        except ImportError:
            print(f"  📥 در حال نصب {package}...")
            os.system(f'pip install {package}')

def main():
    print("🚀 natiq-ultimate - نسخه سبک برای Termux")
    
    # نصب نیازمندی‌ها
    install_requirements()
    
    # تست مدل سبک
    if test_with_simple_model():
        print("\n✅ سیستم آماده است!")
        print("\n💡 راه‌حل‌های پیشنهادی:")
        print("1. PyTorch را با روش Termux نصب کنید")
        print("2. از TensorFlow استفاده کنید")
        print("3. از مدل‌های کاملاً متفاوت استفاده کنید")
        
        # پیشنهاد استفاده از مدل‌های جایگزین
        print("\n🎯 مدل‌های پیشنهادی برای Termux:")
        print("   • distilbert-base-uncased (سبک)")
        print("   • mobilebert-uncased (برای موبایل)")
        print("   • tiny-bert (خیلی سبک)")
    else:
        print("\n❌ نیاز به نصب PyTorch یا TensorFlow دارید")
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
