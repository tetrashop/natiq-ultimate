#!/usr/bin/env python3
"""
natiq-ultimate نسخه کامل - سیستم هوش مصنوعی فارسی پیشرفته
"""

import json
import random
import os
from datetime import datetime
from pathlib import Path

class NatiqComplete:
    def __init__(self):
        # پایگاه دانش جامع فارسی
        self.knowledge_base = self.load_knowledge()
        
        # تاریخچه گفتگو
        self.conversation_history = []
        
        # آمار استفاده
        self.stats = {
            "questions_answered": 0,
            "topics_covered": {},
            "first_use": datetime.now().isoformat()
        }
    
    def load_knowledge(self):
        """بارگذاری پایگاه دانش"""
        return {
            "هوش مصنوعی": {
                "تعریف": "هوش مصنوعی (AI) شاخه‌ای از علوم کامپیوتر است که به ساخت ماشین‌های هوشمند می‌پردازد که می‌توانند مانند انسان فکر کنند، یاد بگیرند و تصمیم بگیرند.",
                "تاریخچه": "مفهوم هوش مصنوعی از دهه ۱۹۵۰ مطرح شد. آلن تورینگ تست تورینگ را پیشنهاد داد که معیاری برای سنجش هوشمندی ماشین‌هاست.",
                "زیرشاخه‌ها": "یادگیری ماشین، پردازش زبان طبیعی، بینایی کامپیوتر، رباتیک، سیستم‌های خبره",
                "کاربردها": "پزشکی (تشخیص بیماری)، خودروسازی (خودروهای خودران)، مالی (تشخیص تقلب)، آموزش (سیستم‌های آموزشی هوشمند)",
                "ابزارها": "پایتون، TensorFlow، PyTorch، scikit-learn"
            },
            "یادگیری ماشین": {
                "تعریف": "یادگیری ماشین (ML) زیرشاخه‌ای از هوش مصنوعی است که به سیستم‌ها توانایی یادگیری خودکار از تجربه و داده‌ها بدون برنامه‌نویسی صریح را می‌دهد.",
                "انواع": "۱. یادگیری نظارت شده ۲. یادگیری نظارت نشده ۳. یادگیری تقویتی",
                "الگوریتم‌ها": "درخت تصمیم، شبکه عصبی، SVM، k-means، رگرسیون خطی",
                "کاربردها": "تشخیص تصویر، پیش‌بینی قیمت‌ها، فیلترینگ ایمیل‌های اسپم، سیستم‌های پیشنهاددهنده"
            },
            "پردازش زبان طبیعی": {
                "تعریف": "پردازش زبان طبیعی (NLP) شاخه‌ای از هوش مصنوعی است که به تعامل بین کامپیوتر و زبان انسان می‌پردازد.",
                "کارها": "ترجمه ماشینی، تحلیل احساسات، خلاصه‌سازی متن، چت بات‌ها، تشخیص موجودیت‌های نامدار",
                "کتابخانه‌ها": "NLTK، spaCy، Transformers، Gensim",
                "چالش‌ها": "ابهام زبانی، تنوع زبانی، نیاز به داده‌های آموزشی زیاد"
            },
            "پایتون": {
                "تعریف": "پایتون یک زبان برنامه‌نویسی سطح بالا، تفسیری، همه‌منظوره و شی‌گرا است که خوانایی بالایی دارد.",
                "کاربردها": "توسعه وب، علم داده، هوش مصنوعی، اتوماسیون، اسکریپت‌نویسی",
                "ویژگی‌ها": "سینتکس ساده، کتابخانه‌های گسترده، جامعه فعال، چندپلتفرمی",
                "کتابخانه‌های معروف": "Django، Flask، NumPy، Pandas، TensorFlow، PyTorch"
            },
            "شبکه عصبی": {
                "تعریف": "شبکه عصبی مصنوعی یک مدل محاسباتی است که از ساختار مغز انسان الهام گرفته شده است.",
                "اجزا": "نورون‌ها، لایه‌ها، وزن‌ها، تابع فعال‌سازی",
                "انواع": "شبکه‌های عصبی پیشخور، شبکه‌های عصبی کانولوشنی، شبکه‌های عصبی بازگشتی",
                "کاربرد": "تشخیص تصویر، پردازش زبان، بازی‌های کامپیوتری"
            }
        }
    
    def understand_question(self, question):
        """درک و تحلیل سوال"""
        q_lower = question.lower()
        
        # تشخیص نوع سوال
        question_types = {
            "چیست": "تعریف",
            "چطور": "روش",
            "چگونه": "روش", 
            "چرا": "دلیل",
            "کی": "زمان",
            "کجا": "مکان",
            "چه": "ویژگی",
            "مزایا": "مزایا",
            "معایب": "معایب"
        }
        
        detected_type = "عمومی"
        for q_type, fa_type in question_types.items():
            if q_type in q_lower:
                detected_type = fa_type
                break
        
        # تشخیص موضوع
        detected_topics = []
        for topic in self.knowledge_base:
            if topic in q_lower:
                detected_topics.append(topic)
        
        return {
            "question": question,
            "type": detected_type,
            "topics": detected_topics,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_answer(self, analysis):
        """تولید پاسخ بر اساس تحلیل سوال"""
        question = analysis["question"]
        q_type = analysis["type"]
        topics = analysis["topics"]
        
        # اگر موضوع خاصی تشخیص داده شد
        if topics:
            topic = topics[0]
            
            if topic in self.knowledge_base:
                topic_info = self.knowledge_base[topic]
                
                # پاسخ بر اساس نوع سوال
                if q_type == "تعریف" and "تعریف" in topic_info:
                    return f"{topic}: {topic_info['تعریف']}"
                elif q_type == "روش" and "کارها" in topic_info:
                    return f"برای {topic} می‌توان این کارها را انجام داد: {topic_info['کارها']}"
                elif q_type == "ویژگی" and "ویژگی‌ها" in topic_info:
                    return f"ویژگی‌های {topic}: {topic_info.get('ویژگی‌ها', topic_info.get('تعریف', ''))}"
                else:
                    # بازگشت اطلاعات کلی
                    keys = list(topic_info.keys())
                    if keys:
                        random_key = random.choice(keys)
                        return f"{topic} ({random_key}): {topic_info[random_key]}"
        
        # پاسخ‌های عمومی هوشمند
        general_responses = [
            f"سوال جالب: '{question}'. من اطلاعاتی در مورد این موضوع دارم.",
            f"درباره '{question}' می‌توانم توضیح دهم. می‌خواهید بیشتر بدانید؟",
            f"این موضوع بخشی از حوزه هوش مصنوعی است. آیا سوال خاص‌تری دارید؟",
            f"برای پاسخ دقیق به '{question}'، لطفاً سوال خود را دقیق‌تر فرمایید."
        ]
        
        return random.choice(general_responses)
    
    def save_conversation(self, question, answer):
        """ذخیره گفتگو"""
        entry = {
            "question": question,
            "answer": answer,
            "timestamp": datetime.now().isoformat()
        }
        self.conversation_history.append(entry)
        
        # ذخیره در فایل
        log_file = Path("logs/conversations.json")
        log_file.parent.mkdir(exist_ok=True)
        
        if log_file.exists():
            with open(log_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
        
        data.append(entry)
        
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def show_statistics(self):
        """نمایش آمار"""
        print("\n📊 آمار natiq-ultimate:")
        print(f"   📅 اولین استفاده: {self.stats['first_use']}")
        print(f"   ❓ سوالات پاسخ داده شده: {self.stats['questions_answered']}")
        print(f"   🗂️  موضوعات پوشش داده شده: {len(self.stats['topics_covered'])}")
        
        if self.stats['topics_covered']:
            print("   🔝 پرکاربردترین موضوعات:")
            for topic, count in sorted(self.stats['topics_covered'].items(), 
                                      key=lambda x: x[1], reverse=True)[:3]:
                print(f"      • {topic}: {count} بار")
    
    def chat_loop(self):
        """حلقه گفتگو"""
        print("🧠 natiq-ultimate - سیستم هوش مصنوعی فارسی کامل")
        print("=" * 70)
        print("ویژگی‌ها:")
        print("• پایگاه دانش جامع فارسی")
        print("• تشخیص هوشمند نوع سوال")
        print("• ذخیره خودکار گفتگوها")
        print("• آمار و گزارش‌گیری")
        print("• بدون نیاز به اینترنت")
        print("=" * 70)
        
        print("\n📝 دستورات ویژه:")
        print("   'آمار' - نمایش آمار استفاده")
        print("   'موضوعات' - لیست موضوعات موجود")
        print("   'خروج' - پایان گفتگو")
        print("-" * 70)
        
        while True:
            try:
                print("\n" + "─" * 40)
                question = input("🧑 شما: ").strip()
                
                if not question:
                    print("⚠️ لطفاً یک سوال وارد کنید")
                    continue
                
                # دستورات ویژه
                if question == "خروج":
                    print("👋 خداحافظ! امیدوارم مفید بوده باشم.")
                    self.show_statistics()
                    break
                elif question == "آمار":
                    self.show_statistics()
                    continue
                elif question == "موضوعات":
                    print("📚 موضوعات موجود در پایگاه دانش:")
                    for topic in self.knowledge_base.keys():
                        print(f"   • {topic}")
                    continue
                
                # تحلیل و پاسخ
                print("🤔 در حال تحلیل سوال...")
                analysis = self.understand_question(question)
                
                # به‌روزرسانی آمار
                self.stats["questions_answered"] += 1
                for topic in analysis["topics"]:
                    self.stats["topics_covered"][topic] = \
                        self.stats["topics_covered"].get(topic, 0) + 1
                
                # تولید پاسخ
                answer = self.generate_answer(analysis)
                
                print(f"🤖 natiq: {answer}")
                
                # نمایش اطلاعات تحلیل
                if analysis["topics"]:
                    print(f"   🏷️  موضوع: {', '.join(analysis['topics'])}")
                print(f"   🎯 نوع سوال: {analysis['type']}")
                
                # ذخیره گفتگو
                self.save_conversation(question, answer)
                
            except KeyboardInterrupt:
                print("\n\n👋 خروج از برنامه...")
                self.show_statistics()
                break
            except Exception as e:
                print(f"❌ خطا: {e}")

def main():
    # ایجاد پوشه‌های لازم
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # اجرای سیستم
    natiq = NatiqComplete()
    natiq.chat_loop()

if __name__ == "__main__":
    main()
