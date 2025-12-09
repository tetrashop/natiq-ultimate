#!/usr/bin/env python3
"""
الگوریتم پیشرفته خروجی‌دهی با مدیریت خودکار پوشه‌ها
ویژگی‌ها:
1. بررسی وجود پوشه و ایجاد خودکار
2. خواندن/نوشتن فایل با پشتیبانی از encoding
3. لاگ‌گیری پیشرفته
4. مدیریت خطا با try-except
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Union, Optional, List, Dict, Any
import json
import yaml

# تنظیمات لاگ‌گیری
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('file_processor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FileProcessor:
    """کلاس مدیریت فایل با قابلیت ایجاد خودکار پوشه‌ها"""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir).resolve()
        self.created_dirs = []
        
    def ensure_directory(self, file_path: Union[str, Path]) -> Path:
        """
        اطمینان از وجود پوشه‌های مسیر فایل
        """
        path = Path(file_path)
        
        # اگر مسیر مطلق نیست، نسبت به base_dir بساز
        if not path.is_absolute():
            path = self.base_dir / path
        
        # ایجاد پوشه‌های والد اگر وجود ندارند
        parent_dir = path.parent
        if not parent_dir.exists():
            parent_dir.mkdir(parents=True, exist_ok=True)
            self.created_dirs.append(str(parent_dir))
            logger.info(f"📁 پوشه ایجاد شد: {parent_dir}")
        
        return path
    
    def read_file(self, file_path: str, encoding: str = 'utf-8') -> str:
        """
        خواندن فایل با بررسی وجود پوشه‌ها
        """
        try:
            path = self.ensure_directory(file_path)
            
            if not path.exists():
                logger.warning(f"⚠️ فایل وجود ندارد: {path}")
                return ""
            
            with open(path, 'r', encoding=encoding) as f:
                content = f.read()
            
            logger.info(f"✅ فایل خوانده شد: {path} ({len(content)} کاراکتر)")
            return content
            
        except Exception as e:
            logger.error(f"❌ خطا در خواندن فایل {file_path}: {str(e)}")
            raise
    
    def write_file(self, file_path: str, content: str, 
                   encoding: str = 'utf-8', mode: str = 'w') -> bool:
        """
        نوشتن در فایل با ایجاد خودکار پوشه‌ها
        """
        try:
            path = self.ensure_directory(file_path)
            
            with open(path, mode, encoding=encoding) as f:
                f.write(content)
            
            logger.info(f"✅ فایل ذخیره شد: {path} ({len(content)} کاراکتر)")
            return True
            
        except Exception as e:
            logger.error(f"❌ خطا در نوشتن فایل {file_path}: {str(e)}")
            return False
    
    def cat_with_info(self, file_path: str, show_stats: bool = True) -> str:
        """
        نمایش محتوای فایل با اطلاعات آماری (شبیه cat پیشرفته)
        """
        content = self.read_file(file_path)
        path = Path(file_path)
        
        if not content:
            return "فایل خالی است یا وجود ندارد"
        
        output = []
        
        if show_stats:
            output.append(f"📊 اطلاعات فایل: {path.name}")
            output.append(f"📁 مسیر کامل: {path.absolute()}")
            output.append(f"📏 حجم فایل: {len(content)} کاراکتر")
            output.append(f"📝 تعداد خطوط: {len(content.splitlines())}")
            output.append(f"🕒 زمان بررسی: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            output.append("-" * 50)
        
        output.append(content)
        
        if show_stats:
            output.append("-" * 50)
            output.append(f"✅ نمایش فایل با موفقیت انجام شد")
        
        return "\n".join(output)
    
    def process_multiple_files(self, file_paths: List[str], 
                               operation: str = 'read') -> Dict[str, Any]:
        """
        پردازش چندین فایل به صورت همزمان
        """
        results = {
            'success': [],
            'failed': [],
            'stats': {
                'total': len(file_paths),
                'processed': 0,
                'created_dirs': self.created_dirs
            }
        }
        
        for file_path in file_paths:
            try:
                if operation == 'read':
                    content = self.read_file(file_path)
                    results['success'].append({
                        'file': file_path,
                        'content_preview': content[:100] + '...' if len(content) > 100 else content
                    })
                elif operation == 'cat':
                    content = self.cat_with_info(file_path)
                    results['success'].append({
                        'file': file_path,
                        'displayed': True
                    })
                
                results['stats']['processed'] += 1
                
            except Exception as e:
                results['failed'].append({
                    'file': file_path,
                    'error': str(e)
                })
        
        return results
    
    def get_directory_tree(self, dir_path: str = ".", max_depth: int = 3) -> str:
        """
        تولید درخت پوشه‌ها و فایل‌ها
        """
        def build_tree(path: Path, prefix: str = "", depth: int = 0) -> List[str]:
            if depth > max_depth:
                return []
            
            lines = []
            try:
                contents = sorted(path.iterdir())
                for i, item in enumerate(contents):
                    is_last = (i == len(contents) - 1)
                    
                    if item.is_dir():
                        lines.append(f"{prefix}{'└── ' if is_last else '├── '}📁 {item.name}/")
                        extension = "    " if is_last else "│   "
                        lines.extend(build_tree(item, prefix + extension, depth + 1))
                    else:
                        lines.append(f"{prefix}{'└── ' if is_last else '├── '}📄 {item.name}")
            except PermissionError:
                lines.append(f"{prefix}└── 🔒 دسترسی محدود")
            
            return lines
        
        root = Path(dir_path).resolve()
        tree_lines = [f"🌳 ساختار پوشه: {root}"]
        tree_lines.extend(build_tree(root))
        return "\n".join(tree_lines)


# تابع کمکی برای استفاده سریع
def cat(file_path: str, create_dirs: bool = True, show_info: bool = True) -> str:
    """
    تابع سریع برای نمایش فایل (شبیه دستور cat لینوکس)
    
    Args:
        file_path: مسیر فایل
        create_dirs: ایجاد خودکار پوشه‌ها اگر وجود ندارند
        show_info: نمایش اطلاعات اضافی
    
    Returns:
        محتوای فایل به صورت رشته
    """
    processor = FileProcessor()
    
    if create_dirs:
        processor.ensure_directory(file_path)
    
    if show_info:
        return processor.cat_with_info(file_path)
    else:
        return processor.read_file(file_path)


def save_json(data: Any, file_path: str, create_dirs: bool = True) -> bool:
    """ذخیره داده در قالب JSON"""
    processor = FileProcessor()
    
    if create_dirs:
        processor.ensure_directory(file_path)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ JSON ذخیره شد: {file_path}")
        return True
    except Exception as e:
        logger.error(f"❌ خطا در ذخیره JSON: {e}")
        return False


def load_json(file_path: str) -> Optional[Dict]:
    """بارگذاری داده از JSON"""
    processor = FileProcessor()
    content = processor.read_file(file_path)
    
    if content:
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"❌ خطا در خواندن JSON: {e}")
    return None


# مثال استفاده
if __name__ == "__main__":
    print("🔧 الگوریتم پیشرفته مدیریت فایل")
    print("=" * 50)
    
    # ایجاد نمونه
    fp = FileProcessor()
    
    # مثال 1: ایجاد پوشه و نمایش فایل
    test_file = "logs/app/test_log.txt"
    content = "این یک فایل تست است.\nتاریخ ایجاد: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if fp.write_file(test_file, content):
        print(f"\n📝 فایل ایجاد شد: {test_file}")
        
        # نمایش با cat پیشرفته
        print("\n" + fp.cat_with_info(test_file))
    
    # مثال 2: نمایش ساختار پوشه
    print("\n" + fp.get_directory_tree(".", max_depth=2))
    
    # مثال 3: پردازش چند فایل
    files_to_process = [
        "data/docs/file1.txt",
        "data/docs/file2.txt",
        "config/settings.json"
    ]
    
    # ایجاد فایل‌های نمونه
    for i, file in enumerate(files_to_process):
        fp.write_file(file, f"محتوای فایل آزمایشی شماره {i+1}\n" * 3)
    
    # پردازش همزمان
    results = fp.process_multiple_files(files_to_process, operation='cat')
    print(f"\n📊 نتایج پردازش:")
    print(f"   موفق: {len(results['success'])}")
    print(f"   ناموفق: {len(results['failed'])}")
    print(f"   پوشه‌های ایجاد شده: {len(results['stats']['created_dirs'])}")
