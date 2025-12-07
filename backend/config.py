"""
تنظیمات پروژه natiq-ultimate
"""

import os
from pathlib import Path

# مسیرهای پروژه
BASE_DIR = Path(__file__).parent.parent
SRC_DIR = BASE_DIR / "src"
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# ایجاد پوشه‌ها اگر وجود ندارند
for directory in [MODELS_DIR, DATA_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# تنظیمات مدل
class ModelConfig:
    """تنظیمات مربوط به مدل‌های هوش مصنوعی"""
    
    # مدل پیش‌فرض برای پردازش فارسی
    DEFAULT_MODEL = "HooshvareLab/bert-base-parsbert-uncased"
    
    # مدل‌های جایگزین
    ALTERNATIVE_MODELS = {
        "light": "HooshvareLab/bert-fa-base-uncased",
        "sentiment": "HooshvareLab/bert-fa-base-uncased-sentiment",
        "ner": "HooshvareLab/bert-fa-base-uncased-ner"
    }
    
    # تنظیمات دانلود
    USE_LOCAL_MODEL = True
    LOCAL_MODEL_PATH = MODELS_DIR / "fa-bert"
    
    # تنظیمات پردازش
    MAX_LENGTH = 512
    BATCH_SIZE = 4

# تنظیمات سیستم
class SystemConfig:
    """تنظیمات مربوط به سیستم"""
    
    # تنظیمات حافظه
    USE_GPU = False  # در Termux معمولا GPU در دسترس نیست
    MAX_MEMORY = "2GB" if not USE_GPU else "8GB"
    
    # تنظیمات لاگ
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # تنظیمات ذخیره‌سازی
    CACHE_DIR = MODELS_DIR / ".cache"
    SAVE_INTERVAL = 100  # ذخیره هر ۱۰۰ پردازش

# تنظیمات امنیتی
class SecurityConfig:
    """تنظیمات امنیتی"""
    
    API_KEY = os.getenv("NATIQ_API_KEY", "")
    ENABLE_AUTH = False
    ALLOWED_ORIGINS = ["*"]

# دسترسی آسان به تنظیمات
settings = {
    "model": ModelConfig(),
    "system": SystemConfig(),
    "security": SecurityConfig(),
    "paths": {
        "base": BASE_DIR,
        "models": MODELS_DIR,
        "data": DATA_DIR,
        "logs": LOGS_DIR,
        "src": SRC_DIR
    }
}
