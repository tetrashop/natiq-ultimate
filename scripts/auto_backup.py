#!/usr/bin/env python3
"""
اسکریپت پشتیبان‌گیری خودکار
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
import tarfile
import hashlib
import sys

class AutoBackup:
    def __init__(self, backup_dir="./backups", max_backups=10):
        self.backup_dir = Path(backup_dir)
        self.max_backups = max_backups
        self.backup_dir.mkdir(exist_ok=True)
        
    def create_backup(self):
        """ایجاد پشتیبان کامل"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"natiq_backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        
        # لیست فایل‌ها برای پشتیبان
        files_to_backup = [
            "src/",
            "api/",
            "models/",
            "data/",
            "logs/",
            "*.py",
            "*.json",
            "*.txt",
            "*.md",
            "*.sh"
        ]
        
        # فایل tar.gz
        tar_path = backup_path.with_suffix(".tar.gz")
        
        try:
            print(f"📦 ایجاد پشتیبان: {tar_path.name}")
            
            with tarfile.open(tar_path, "w:gz") as tar:
                # اضافه کردن فایل‌ها
                for pattern in files_to_backup:
                    if "*" in pattern:
                        # فایل‌های با الگو
                        for file in Path(".").glob(pattern):
                            if file.is_file():
                                tar.add(file)
                                print(f"  📄 {file}")
                    else:
                        # پوشه‌ها
                        folder = Path(pattern.rstrip("/"))
                        if folder.exists():
                            tar.add(folder)
                            print(f"  📁 {folder}/")
            
            # محاسبه hash
            file_hash = self.calculate_hash(tar_path)
            
            # ذخیره metadata
            metadata = {
                "timestamp": timestamp,
                "filename": tar_path.name,
                "size": tar_path.stat().st_size,
                "hash": file_hash,
                "files": [str(f) for f in Path(".").glob("**/*") if f.is_file()]
            }
            
            metadata_path = backup_path.with_suffix(".json")
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)
            
            print(f"✅ پشتیبان ایجاد شد: {tar_path.stat().st_size / 1024 / 1024:.2f} MB")
            print(f"🔒 Hash: {file_hash}")
            
            # حذف پشتیبان‌های قدیمی
            self.cleanup_old_backups()
            
            return True
            
        except Exception as e:
            print(f"❌ خطا در ایجاد پشتیبان: {e}")
            return False
    
    def calculate_hash(self, file_path: Path) -> str:
        """محاسبه hash فایل"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def cleanup_old_backups(self):
        """حذف پشتیبان‌های قدیمی"""
        backups = list(self.backup_dir.glob("natiq_backup_*.tar.gz"))
        backups.sort(key=os.path.getmtime)
        
        if len(backups) > self.max_backups:
            to_delete = backups[:-self.max_backups]
            for backup in to_delete:
                # حذف فایل tar.gz و json مربوطه
                backup.unlink()
                json_file = backup.with_suffix(".json")
                if json_file.exists():
                    json_file.unlink()
                
                print(f"🗑️  حذف پشتیبان قدیمی: {backup.name}")

if __name__ == "__main__":
    backup = AutoBackup(max_backups=20)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        # حالت خودکار (برای cron job)
        backup.create_backup()
    else:
        # حالت تعاملی
        print("🔧 ابزار پشتیبان‌گیری natiq-ultimate")
        print("=" * 50)
        
        while True:
            print("\nگزینه‌ها:")
            print("  1. ایجاد پشتیبان جدید")
            print("  2. مشاهده پشتیبان‌های موجود")
            print("  3. خروج")
            
            choice = input("\nانتخاب شما: ").strip()
            
            if choice == "1":
                backup.create_backup()
            elif choice == "2":
                backups = list(backup.backup_dir.glob("*.tar.gz"))
                if backups:
                    print(f"\n📚 {len(backups)} پشتیبان موجود:")
                    for b in sorted(backups, reverse=True):
                        size = b.stat().st_size / 1024 / 1024
                        print(f"  • {b.name} ({size:.1f} MB)")
                else:
                    print("هیچ پشتیبان‌ای یافت نشد")
            elif choice == "3":
                print("خروج...")
                break
            else:
                print("گزینه نامعتبر")
