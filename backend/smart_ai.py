#!/usr/bin/env python3
"""
هوش مصنوعی هوشمند برای Termux - بدون نیاز به TensorFlow/PyTorch
"""

import json
import random
import requests
from datetime import datetime

class NatiqAI:
    """دستیار هوشمند فارسی با قابلیت‌های پیشرفته"""
    
    def __init__(self):
        # پایگاه دانش گسترده
        self.knowledge_base = {
            "هوش مصنوعی": {
                "تعریف": "هوش مصنوعی (AI) شاخه‌ای از علوم کامپیوتر است که به ساخت ماشین‌های هوشمند می‌پردازد.",
                "زیرشاخه‌ها": "شامل یادگیری ماشین، پردازش زبان طبیعی، بینایی کامپیوتر و رباتیک می‌شود.",
                "کاربردها": "در پزشکی، خودروسازی، مالی، آموزش و بسیاری صنایع دیگر استفاده می‌شود."
            },
            "یادگیری ماشین": {
                "تعریف": "یادگیری ماشین (ML) زیرشاخه‌ای از AI است که به سیستم‌ها توانایی یادگیری از داده می‌دهد.",
                "انواع": "شامل یادگیری نظارت شده، نظارت نشده و تقویتی می‌شود."
            },
            "پردازش زبان طبیعی": {
                "تعریف": "NLP شاخه‌ای از AI است که به تعامل کامپیوتر و زبان انسان می‌پردازد.",
                "کاربردها": "ترجمه ماشینی، چت بات‌ها، تحلیل احساسات و خلاصه‌سازی متن"
            }
        }
        
        # الگوهای پاسخ
        self.patterns = {
            "سلام": ["سلام! خوش آمدید.", "درود! چطور می‌تونم کمک کنم؟"],
            "حال": ["من یک برنامه کامپیوتری هستم، اما ممنون که پرسیدید!", "خوبم! شما چطورید؟"],
            "اسم": ["من natiq-ultimate هستم، دستیار هوشمند فارسی شما!"],
            "ساعت": lambda: f"الان ساعت {datetime.now().strftime('%H:%M')} است.",
            "تاریخ": lambda: f"امروز {datetime.now().strftime('%Y/%m/%d')} است.",
            "ممنون": ["خواهش می‌کنم!", "خوشحالم که مفید بودم!"]
        }
    
    def analyze_question(self, question):
        """تحلیل سوال و استخراج موضوع اصلی"""
        question_lower = question.lower()
        
        # تشخیص موضوع
        topics = []
        for topic in self.knowledge_base:
            if topic in question_lower:
                topics.append(topic)
        
        return topics
    
    def generate_response(self, question):
        """تولید پاسخ هوشمند"""
        topics = self.analyze_question(question)
        
        # اگر موضوع خاصی تشخیص داده شد
        if topics:
            topic = topics[0]
            subtopics = list(self.knowledge_base[topic].keys())
            
            if len(subtopics) > 0:
                # انتخاب یک زیرموضوع تصادفی یا جواب کامل
                if "چیست" in question or " چیست" in question:
                    return f"{topic}: {self.knowledge_base[topic]['تعریف']}"
                else:
                    subtopic = random.choice(subtopics)
                    return f"{topic} ({subtopic}): {self.knowledge_base[topic][subtopic]}"
        
        # بررسی الگوهای خاص
        for pattern, response in self.patterns.items():
            if pattern in question.lower():
                if callable(response):
                    return response()
                else:
                    return random.choice(response)
        
        # پاسخ پیشرفته برای سوالات مختلف
        question_words = question.lower().split()
        
        if "چرا" in question:
            return "این یک سوال فلسفی جالب است! پاسخ دقیق نیاز به بررسی بیشتر دارد."
        elif "چطور" in question or "چگونه" in question:
            return "برای انجام این کار، می‌توانید مراحل مختلفی را دنبال کنید."
        elif "کی" in question:
            return "زمان دقیق بستگی به شرایط مختلف دارد."
        elif "کجا" in question:
            return "مکان آن در فضای دیجیتال است!"
        
        # پاسخ پیش‌فرض
        responses = [
            f"سوال جالبی پرسیدید: '{question}'. من در حال یادگیری بیشتر در این زمینه هستم!",
            "لطفاً سوال خود را دقیق‌تر بپرسید تا بتوانم کمک بهتری کنم.",
            "این موضوع برای من جالب است. می‌توانید اطلاعات بیشتری بدهید؟",
            "من نسخه ساده natiq هستم. برای پاسخ‌های پیشرفته‌تر نیاز به نصب کتابخانه‌های اضافی دارم."
        ]
        
        return random.choice(responses)
    
    def get_external_info(self, query):
        """دریافت اطلاعات از منابع خارجی (اگر اینترنت داشته باشید)"""
        try:
            # استفاده از DuckDuckGo Instant Answer API
            response = requests.get(
                f"https://api.duckduckgo.com/?q={query}&format=json&pretty=1",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                if data['Abstract']:
                    return data['Abstract'][:200] + "..."
        except:
            pass
        
        return None

def main():
    print("🧠 natiq-ultimate - نسخه هوشمند")
    print("=" * 60)
    print("ویژگی‌ها:")
    print("• پایگاه دانش گسترده فارسی")
    print("• تشخیص خودکار موضوع سوال")
    print("• پاسخ‌های هوشمند و متنوع")
    print("• بدون نیاز به TensorFlow/PyTorch")
    print("=" * 60)
    
    ai = NatiqAI()
    
    while True:
        try:
            print("\n" + "-" * 40)
            question = input("📝 سوال شما: ").strip()
            
            if question.lower() in ['خروج', 'exit', 'quit']:
                print("👋 خداحافظ! موفق باشید.")
                break
            
            if not question:
                print("⚠️ لطفاً یک سوال وارد کنید")
                continue
            
            print("🤔 در حال تحلیل سوال...")
            
            # بررسی اطلاعات خارجی (اگر اینترنت باشد)
            external_answer = ai.get_external_info(question)
            if external_answer:
                print(f"🌐 از منابع آنلاین: {external_answer}")
            else:
                # تولید پاسخ محلی
                answer = ai.generate_response(question)
                print(f"🤖 natiq: {answer}")
            
            # نمایش موضوعات تشخیص داده شده
            topics = ai.analyze_question(question)
            if topics:
                print(f"🏷️  موضوعات تشخیص داده شده: {', '.join(topics)}")
            
        except KeyboardInterrupt:
            print("\n👋 خروج از برنامه...")
            break
        except Exception as e:
            print(f"❌ خطا: {e}")

if __name__ == "__main__":
    main()
