#!/usr/bin/env python3
"""
نمونه‌های استفاده از الگوریتم مدیریت فایل در پروژه natiq-ultimate
"""

from advanced_file_processor import cat, FileProcessor, save_json, load_json

# مثال 1: خواندن لاگ‌های API با ایجاد خودکار پوشه
def read_api_logs():
    """خواندن فایل لاگ با ایجاد خودکار پوشه‌ها"""
    log_content = cat('logs/api/requests.log', create_dirs=True)
    print("📊 لاگ‌های API:")
    print(log_content[:500] + "..." if len(log_content) > 500 else log_content)

# مثال 2: ذخیره تنظیمات کاربر
def save_user_settings(user_id: str, settings: dict):
    """ذخیره تنظیمات کاربر در فایل JSON"""
    file_path = f"data/users/{user_id}/settings.json"
    success = save_json(settings, file_path, create_dirs=True)
    if success:
        print(f"✅ تنظیمات کاربر {user_id} ذخیره شد")
    return success

# مثال 3: بارگذاری پیکربندی
def load_config():
    """بارگذاری پیکربندی پروژه"""
    config = load_json("config/project/config.json")
    if not config:
        # ایجاد پیکربندی پیش‌فرض
        default_config = {
            "name": "natiq-ultimate",
            "version": "1.0.0",
            "api_endpoint": "/api/v1",
            "debug": False,
            "log_level": "INFO"
        }
        save_json(default_config, "config/project/config.json", create_dirs=True)
        return default_config
    return config

# مثال 4: نمایش ساختار پروژه
def show_project_structure():
    """نمایش درخت پوشه‌های پروژه"""
    processor = FileProcessor()
    tree = processor.get_directory_tree(".", max_depth=4)
    print(tree)

# مثال 5: پردازش گروهی فایل‌های ترجمه
def process_translation_files():
    """پردازش چندین فایل ترجمه"""
    processor = FileProcessor("translations")
    
    files = [
        "fa/strings.json",
        "en/strings.json",
        "ar/strings.json"
    ]
    
    # ایجاد فایل‌های نمونه ترجمه
    translations = {
        "fa": {"hello": "سلام", "goodbye": "خداحافظ"},
        "en": {"hello": "Hello", "goodbye": "Goodbye"},
        "ar": {"hello": "مرحبا", "goodbye": "مع السلامة"}
    }
    
    for lang, trans in translations.items():
        processor.write_file(f"{lang}/strings.json", json.dumps(trans, ensure_ascii=False, indent=2))
    
    # پردازش همزمان
    results = processor.process_multiple_files(files, operation='read')
    print(f"📊 نتایج پردازش فایل‌های ترجمه:")
    print(f"   کل فایل‌ها: {results['stats']['total']}")
    print(f"   موفق: {len(results['success'])}")
    
    for success in results['success']:
        print(f"   ✓ {success['file']}")

# مثال استفاده در FastAPI
if __name__ == "__main__":
    print("🚀 نمونه‌های استفاده از الگوریتم در natiq-ultimate")
    print("=" * 60)
    
    # تست توابع
    read_api_logs()
    print("\n" + "=" * 60)
    
    show_project_structure()
    print("\n" + "=" * 60)
    
    # ذخیره تنظیمات نمونه کاربر
    sample_settings = {
        "theme": "dark",
        "language": "fa",
        "notifications": True,
        "timezone": "Asia/Tehran"
    }
    save_user_settings("user_123", sample_settings)
    
    print("\n" + "=" * 60)
    process_translation_files()
    
    print("\n" + "=" * 60)
    config = load_config()
    print(f"⚙️  پیکربندی پروژه: {config['name']} v{config['version']}")
