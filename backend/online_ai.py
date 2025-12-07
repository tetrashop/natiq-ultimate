#!/usr/bin/env python3
"""
نسخه آنلاین natiq - استفاده از APIهای رایگان
"""

import requests
import json

class OnlineNatiq:
    def __init__(self):
        self.apis = {
            "huggingface": "https://api-inference.huggingface.co/models/google/flan-t5-small",
            "duckduckgo": "https://api.duckduckgo.com/"
        }
    
    def ask(self, question):
        print(f"🌐 جستجوی آنلاین برای: {question}")
        
        # ابتدا DuckDuckGo را امتحان کن
        try:
            response = requests.get(
                f"{self.apis['duckduckgo']}?q={question}&format=json&pretty=1",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('Abstract'):
                    return f"📚 از دانش‌نامه: {data['Abstract'][:250]}..."
        except:
            pass
        
        return "🌐 (نیاز به تنظیم API key برای پاسخ‌های آنلاین پیشرفته)"

# تست سریع
if __name__ == "__main__":
    ai = OnlineNatiq()
    print(ai.ask("هوش مصنوعی چیست؟"))
