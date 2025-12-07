#!/usr/bin/env python3
"""
natiq-ultimate - نسخه مبتنی بر فایل‌های دانش
"""

import json
import os
from pathlib import Path

class FileBasedAI:
    def __init__(self):
        self.data_dir = Path("data/knowledge")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.load_or_create_knowledge()
    
    def load_or_create_knowledge(self):
        """بارگذاری یا ایجاد فایل‌های دانش"""
        default_knowledge = {
            "ai.json": {
                "موضوع": "هوش مصنوعی",
                "تعاریف": [
                    "هوش مصنوعی شاخه‌ای از علوم کامپیوتر است که به ساخت ماشین‌های هوشمند می‌پردازد.",
                    "AI توانایی یک سیستم برای درک محیط و انجام اقداماتی است که شانس موفقیت آن را افزایش می‌دهد."
                ],
                "کاربردها": ["پزشکی", "مالی", "آموزش", "ترابری"],
                "کلمات_کلیدی": ["هوش مصنوعی", "AI", "ماشین هوشمند"]
            },
            "ml.json": {
                "موضوع": "یادگیری ماشین",
                "تعاریف": [
                    "یادگیری ماشین زیرشاخه‌ای از هوش مصنوعی است که به سیستم‌ها توانایی یادگیری خودکار می‌دهد.",
                    "ML استفاده از الگوریتم‌هایی است که از داده‌ها یاد می‌گیرند و پیش‌بینی می‌کنند."
                ],
                "الگوریتم‌ها": ["درخت تصمیم", "شبکه عصبی", "SVM"],
                "کلمات_کلیدی": ["یادگیری ماشین", "ML", "الگوریتم"]
            }
        }
        
        # ایجاد فایل‌های پیش‌فرض
        for filename, content in default_knowledge.items():
            file_path = self.data_dir / filename
            if not file_path.exists():
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(content, f, ensure_ascii=False, indent=2)
                print(f"📁 فایل {filename} ایجاد شد")
    
    def search_knowledge(self, question):
        """جستجو در فایل‌های دانش"""
        results = []
        
        for file_path in self.data_dir.glob("*.json"):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
                # جستجو در کلمات کلیدی
                keywords = data.get("کلمات_کلیدی", [])
                for keyword in keywords:
                    if keyword.lower() in question.lower():
                        results.append({
                            "موضوع": data["موضوع"],
                            "تعریف": data["تعاریف"][0] if data.get("تعاریف") else "",
                            "فایل": file_path.name
                        })
                        break
        
        return results
    
    def add_knowledge(self, topic, definition):
        """افزودن دانش جدید"""
        filename = f"{topic.replace(' ', '_')}.json"
        file_path = self.data_dir / filename
        
        new_knowledge = {
            "موضوع": topic,
            "تعاریف": [definition],
            "کلمات_کلیدی": [topic]
        }
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(new_knowledge, f, ensure_ascii=False, indent=2)
        
        print(f"✅ دانش جدید اضافه شد: {topic}")
    
    def chat(self):
        """گفتگو با کاربر"""
        print("📚 natiq-ultimate - سیستم دانش مبتنی بر فایل")
        print("=" * 60)
        
        while True:
            question = input("\nسوال شما: ").strip()
            
            if question.lower() in ["خروج", "exit"]:
                print("خداحافظ!")
                break
            
            results = self.search_knowledge(question)
            
            if results:
                print(f"\n🔍 {len(results)} نتیجه یافت شد:")
                for i, result in enumerate(results, 1):
                    print(f"\n{i}. موضوع: {result['موضوع']}")
                    print(f"   تعریف: {result['تعریف']}")
            else:
                print("\n❌ پاسخی یافت نشد.")
                add_new = input("آیا می‌خواهید دانش جدید اضافه کنید؟ (بله/خیر): ")
                if add_new.lower() in ["بله", "yes", "y"]:
                    topic = input("موضوع چیست؟ ")
                    definition = input("تعریف آن چیست؟ ")
                    self.add_knowledge(topic, definition)

if __name__ == "__main__":
    ai = FileBasedAI()
    ai.chat()
