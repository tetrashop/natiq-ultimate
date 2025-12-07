#!/usr/bin/env python3
"""
استفاده از APIهای رایگان بدون نیاز به کلید
"""

import requests
import urllib.parse

class FreeAPI:
    def ask_wikipedia(self, question):
        """استفاده از ویکی‌پدیا"""
        try:
            url = f"https://fa.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={urllib.parse.quote(question)}&utf8=1"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get('query', {}).get('search'):
                first_result = data['query']['search'][0]
                return f"از ویکی‌پدیا: {first_result['snippet']}..."
        except:
            pass
        return None
    
    def ask_duckduckgo(self, question):
        """استفاده از DuckDuckGo Instant Answer"""
        try:
            url = f"http://api.duckduckgo.com/?q={urllib.parse.quote(question)}&format=json&no_html=1"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get('AbstractText'):
                return f"دانش‌نامه: {data['AbstractText']}"
        except:
            pass
        return None
    
    def ask(self, question):
        """پرسش از تمام APIها"""
        print(f"🔍 جستجو برای: {question}")
        
        # اول DuckDuckGo
        answer = self.ask_duckduckgo(question)
        if answer:
            return answer
        
        # سپس ویکی‌پدیا
        answer = self.ask_wikipedia(question)
        if answer:
            return answer
        
        return "متأسفم نتوانستم پاسخ آنلاین پیدا کنم. آیا سوال دیگری دارید؟"

# تست
if __name__ == "__main__":
    api = FreeAPI()
    print(api.ask("هوش مصنوعی"))
    print("\n" + "="*50 + "\n")
    print(api.ask("پایتون"))
