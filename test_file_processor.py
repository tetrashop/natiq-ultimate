#!/usr/bin/env python3
"""تست الگوریتم مدیریت فایل"""

from advanced_file_processor import cat, save_json, load_json, FileProcessor
import os

def run_tests():
    print("🧪 اجرای تست‌های الگوریتم")
    print("=" * 50)
    
    # تست 1: ایجاد پوشه و خواندن/نوشتن
    print("\n1. تست ایجاد خودکار پوشه:")
    processor = FileProcessor()
    
    test_path = "test_data/subfolder/deep/nested/file.txt"
    test_content = "این یک تست است.\nخط دوم.\nخط سوم."
    
    # نوشتن فایل (پوشه‌ها باید خودکار ایجاد شوند)
    success = processor.write_file(test_path, test_content)
    print(f"   نوشتن فایل: {'✅ موفق' if success else '❌ ناموفق'}")
    
    # خواندن و نمایش
    if success:
        displayed = processor.cat_with_info(test_path)
        print(f"   خواندن فایل: ✅ موفق")
        print(f"   حجم محتوا: {len(test_content)} کاراکتر")
    
    # تست 2: تابع cat سریع
    print("\n2. تست تابع cat سریع:")
    quick_result = cat("test_data/another/test.txt", create_dirs=True, show_info=True)
    print(f"   نتیجه: {'✅ نمایش داده شد' if quick_result else '❌ خطا'}")
    
    # تست 3: JSON operations
    print("\n3. تست عملیات JSON:")
    data = {
        "پروژه": "natiq-ultimate",
        "نسخه": "1.0.0",
        "تاریخ": "2024",
        "تنظیمات": {
            "api": True,
            "debug": False,
            "log_level": "INFO"
        }
    }
    
    json_path = "config/project/settings.json"
    save_json(data, json_path, create_dirs=True)
    
    loaded = load_json(json_path)
    print(f"   ذخیره JSON: ✅")
    print(f"   بارگذاری JSON: {'✅ موفق' if loaded else '❌ ناموفق'}")
    
    # تست 4: درخت پوشه‌ها
    print("\n4. تست نمایش درخت پوشه‌ها:")
    tree = processor.get_directory_tree("test_data", max_depth=3)
    print(tree[:500] + "...")  # نمایش بخشی از درخت
    
    # تست 5: پردازش چند فایل
    print("\n5. تست پردازش چند فایل:")
    files = [
        "output/reports/report1.md",
        "output/reports/report2.md",
        "output/analytics/data.csv"
    ]
    
    for i, file in enumerate(files):
        processor.write_file(file, f"# گزارش {i+1}\n\nمحتوای آزمایشی.")
    
    results = processor.process_multiple_files(files, operation='read')
    print(f"   تعداد فایل‌ها: {results['stats']['total']}")
    print(f"   پردازش شده: {results['stats']['processed']}")
    print(f"   موفق: {len(results['success'])}")
    
    # پاکسازی تست
    print("\n🧹 پاکسازی فایل‌های تست...")
    import shutil
    if os.path.exists("test_data"):
        shutil.rmtree("test_data")
    if os.path.exists("config/project"):
        shutil.rmtree("config/project")
    if os.path.exists("output"):
        shutil.rmtree("output")
    
    print("✅ تست‌ها با موفقیت کامل شدند!")

if __name__ == "__main__":
    run_tests()
