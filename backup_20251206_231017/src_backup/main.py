#!/usr/bin/env python3
"""
natiq-ultimate - سیستم هوش مصنوعی پردازش زبان فارسی
ورودی: متن فارسی
خروجی: پاسخ هوش مصنوعی
"""

import os
import sys
import logging
from pathlib import Path

# اضافه کردن مسیر src به sys.path
sys.path.append(str(Path(__file__).parent))

from config import settings
from core.nlp_processor import NLPProcessor
from utils.logger import setup_logger

def main():
    """تابع اصلی اجرای برنامه"""
    # راه‌اندازی لاگر
    logger = setup_logger(__name__)
    logger.info("🚀 راه‌اندازی natiq-ultimate")
    
    try:
        # بررسی محیط اجرا
        logger.info(f"پایتون {sys.version}")
        logger.info(f"مسیر کار: {os.getcwd()}")
        
        # بررسی کتابخانه‌های ضروری
        required_libs = ['torch', 'transformers', 'numpy']
        for lib in required_libs:
            try:
                __import__(lib)
                logger.info(f"✅ {lib} بارگذاری شد")
            except ImportError:
                logger.error(f"❌ {lib} یافت نشد. لطفا نصب کنید.")
                return 1
        
        # ایجاد پردازشگر NLP
        logger.info("در حال راه‌اندازی پردازشگر NLP...")
        nlp_processor = NLPProcessor()
        
        # تست سیستم
        test_text = "سلام، چطوری؟"
        logger.info(f"تست سیستم با متن: {test_text}")
        
        # پردازش متن (در آینده کامل می‌شود)
        response = nlp_processor.process(test_text)
        logger.info(f"پاسخ سیستم: {response}")
        
        logger.info("✅ سیستم با موفقیت راه‌اندازی شد")
        return 0
        
    except Exception as e:
        logger.error(f"خطا در اجرای برنامه: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
