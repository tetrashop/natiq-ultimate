"""
مدیریت لاگ‌گیری
"""

import logging
import sys
from pathlib import Path
from ..config import settings

def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    """
    راه‌اندازی logger
    
    Args:
        name: نام logger
        log_file: مسیر فایل لاگ (اختیاری)
    
    Returns:
        logger تنظیم شده
    """
    # ایجاد logger
    logger = logging.getLogger(name)
    
    # تنظیم سطح لاگ
    log_level = getattr(logging, settings["system"].LOG_LEVEL)
    logger.setLevel(log_level)
    
    # اگر logger قبلا تنظیم شده، از تنظیم مجدد جلوگیری کن
    if logger.handlers:
        return logger
    
    # فرمت‌دهنده
    formatter = logging.Formatter(settings["system"].LOG_FORMAT)
    
    # handler برای کنسول
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # handler برای فایل (اگر مشخص شده)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        # فایل لاگ پیش‌فرض
        log_dir = settings["paths"]["logs"]
        log_file = log_dir / f"{name}.log"
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
