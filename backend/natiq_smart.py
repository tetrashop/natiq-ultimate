#!/usr/bin/env python3
"""
natiq-ultimate نسخه هوشمند - با قابلیت یادگیری و پاسخ‌های شخصی
"""

import json
import os
import random
from datetime import datetime
from pathlib import Path

class NatiqSmart:
    def __init__(self):
        self.user_name = None
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # مسیرهای فایل
        self.data_dir = Path("data")
        self.knowledge_file = self.data_dir / "knowledge.json"
        self.conversations_file = self.data_dir / "conversations.json"
        self.learned_file = self.data_dir / "learned.json"
        
        # ایجاد پوشه‌ها
        self.data_dir.mkdir(exist_ok=True)
        
        # بارگذاری داده‌ها
        self.knowledge = self.load_knowledge()
        self.learned = self.load_learned()
        
        # آمار
        self.stats = {
            "session_start": datetime.now().isoformat(),
            "questions_asked": 0,
            "topics_covered": set(),
            "unknown_questions": []
        }
    
    def load_knowledge(self):
        """بارگذاری پایگاه دانش"""
        default_knowledge = {
            "سیستم": {
                "اسم": "من natiq-ultimate هستم، یک دستیار هوشمند فارسی.",
                "سازنده": "توسط تیم توسعه tetrashop ایجاد شده‌ام.",
                "هدف": "هدف من کمک به کاربران فارسی‌زبان در زمینه هوش مصنوعی و فناوری است.",
                "دسترسی": "من فقط به اطلاعاتی که شما به من می‌دهید دسترسی دارم. به فایل‌های شخصی شما دسترسی ندارم.",
                "حریم خصوصی": "همه گفتگوها محرمانه است و فقط برای بهبود سیستم استفاده می‌شود."
            },
            "هوش مصنوعی": {
                "تعریف": "هوش مصنوعی (AI) علم ساخت ماشین‌های هوشمند است که می‌توانند مانند انسان فکر کنند و یاد بگیرند.",
                "زیرشاخه": ["یادگیری ماشین", "پردازش زبان طبیعی", "بینایی کامپیوتر", "رباتیک"],
                "کاربرد": ["پزشکی", "مالی", "آموزش", "خودروسازی", "امنیت"]
            },
            "پایتون": {
                "تعریف": "پایتون یک زبان برنامه‌نویسی سطح بالا، تفسیری و همه‌منظوره است.",
                "استفاده": ["وب", "هوش مصنوعی", "علم داده", "اتوماسیون"],
                "کتابخانه": ["Django", "Flask", "TensorFlow", "PyTorch", "Pandas"]
            }
        }
        
        if self.knowledge_file.exists():
            with open(self.knowledge_file, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            with open(self.knowledge_file, "w", encoding="utf-8") as f:
                json.dump(default_knowledge, f, ensure_ascii=False, indent=2)
            return default_knowledge
    
    def load_learned(self):
        """بارگذاری دانش آموخته شده"""
        if self.learned_file.exists():
            with open(self.learned_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def save_learned(self, question, answer):
        """ذخیره دانش جدید"""
        self.learned[question.lower()] = answer
        
        with open(self.learned_file, "w", encoding="utf-8") as f:
            json.dump(self.learned, f, ensure_ascii=False, indent=2)
    
    def save_conversation(self, question, answer):
        """ذخیره گفتگو"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer,
            "session": self.session_id
        }
        
        data = []
        if self.conversations_file.exists():
            with open(self.conversations_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        
        data.append(entry)
        
        with open(self.conversations_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def analyze_question(self, question):
        """تحلیل عمیق سوال"""
        q_lower = question.lower()
        
        # کلمات کلیدی
        keywords = {
            "کیستی": {"type": "هویت", "topic": "سیستم"},
            "اسم": {"type": "هویت", "topic": "سیستم"},
            "چیستی": {"type": "تعریف", "topic": "عمومی"},
            "چیست": {"type": "تعریف", "topic": "عمومی"},
            "چطور": {"type": "روش", "topic": "عمومی"},
            "چگونه": {"type": "روش", "topic": "عمومی"},
            "چرا": {"type": "دلیل", "topic": "عمومی"},
            "آیا": {"type": "تأیید", "topic": "عمومی"},
            "دسترسی": {"type": "امنیت", "topic": "سیستم"},
            "می‌شناسی": {"type": "شناخت", "topic": "کاربر"},
            "مرا": {"type": "شناخت", "topic": "کاربر"},
            "من": {"type": "شناخت", "topic": "کاربر"},
            "تو": {"type": "هویت", "topic": "سیستم"}
        }
        
        # تشخیص نوع و موضوع
        detected_type = "عمومی"
        detected_topic = "عمومی"
        
        for keyword, info in keywords.items():
            if keyword in q_lower:
                detected_type = info["type"]
                detected_topic = info["topic"]
                break
        
        # تشخیص موضوع از دانش
        for topic in self.knowledge:
            if topic in q_lower:
                detected_topic = topic
                break
        
        return {
            "text": question,
            "type": detected_type,
            "topic": detected_topic,
            "words": len(question.split()),
            "has_question_mark": "؟" in question or "?" in question
        }
    
    def generate_answer(self, question, analysis):
        """تولید پاسخ هوشمند"""
        q_lower = question.lower()
        
        # 1. اول بررسی دانش آموخته شده
        if q_lower in self.learned:
            return self.learned[q_lower]
        
        # 2. بررسی سوالات سیستمی
        if analysis["topic"] == "سیستم":
            if "اسم" in q_lower or "کیستی" in q_lower or "تو" in q_lower:
                return self.knowledge["سیستم"]["اسم"]
            elif "دسترسی" in q_lower or "فایل" in q_lower:
                return self.knowledge["سیستم"]["دسترسی"]
            elif "حریم" in q_lower or "خصوصی" in q_lower:
                return self.knowledge["سیستم"]["حریم خصوصی"]
            elif "سازنده" in q_lower:
                return self.knowledge["سیستم"]["سازنده"]
        
        # 3. بررسی سوالات شناختی (کاربر)
        if analysis["type"] == "شناخت":
            if self.user_name:
                return f"بله، شما {self.user_name} هستید. چطور می‌تونم کمک کنم؟"
            else:
                return "هنوز شما را نمی‌شناسم. اگر دوست دارید، اسم شما چیست؟"
        
        # 4. بررسی پایگاه دانش اصلی
        if analysis["topic"] in self.knowledge:
            topic_data = self.knowledge[analysis["topic"]]
            
            if analysis["type"] == "تعریف" and "تعریف" in topic_data:
                return f"{analysis['topic']}: {topic_data['تعریف']}"
            elif analysis["type"] == "روش" and "استفاده" in topic_data:
                uses = ", ".join(topic_data["استفاده"]) if isinstance(topic_data["استفاده"], list) else topic_data["استفاده"]
                return f"از {analysis['topic']} در این زمینه‌ها استفاده می‌شود: {uses}"
        
        # 5. پاسخ‌های هوشمند بر اساس نوع سوال
        smart_responses = {
            "تعریف": [
                f"درباره '{question}' می‌توانم بگویم که...",
                f"این یک سوال تعریفی خوب است. '{question}' به این معناست که...",
                f"برای تعریف '{question}' نیاز به اطلاعات بیشتری دارم."
            ],
            "روش": [
                f"برای انجام '{question}' می‌توان این مراحل را دنبال کرد...",
                f"روش انجام '{question}' بستگی به شرایط دارد.",
                f"می‌خواهید روش دقیق '{question}' را بدانید؟"
            ],
            "دلیل": [
                f"دلیل '{question}' می‌تواند چند چیز باشد...",
                f"این سوال فلسفی است! دلیل '{question}'...",
                f"برای پاسخ به 'چرا {question}' نیاز به تحلیل بیشتری دارم."
            ],
            "تأیید": [
                f"بستگی دارد که منظورتون از '{question}' چیست.",
                f"می‌توانم بگویم که '{question}' در برخی شرایط درست است.",
                f"برای تأیید یا رد '{question}' نیاز به شواهد دارم."
            ]
        }
        
        if analysis["type"] in smart_responses:
            responses = smart_responses[analysis["type"]]
            return random.choice(responses)
        
        # 6. پاسخ پیش‌فرض با قابلیت یادگیری
        return self.handle_unknown_question(question)
    
    def handle_unknown_question(self, question):
        """مدیریت سوالات ناشناخته"""
        self.stats["unknown_questions"].append(question)
        
        responses = [
            f"سوال جالبی پرسیدید: '{question}'. می‌خواهید چه پاسخی بدهم؟",
            f"هنوز پاسخی برای '{question}' ندارم. دوست دارید چه بگویم؟",
            f"این سوال جدیدی برای من است. پیشنهاد شما برای پاسخ چیست؟",
            f"درباره '{question}' اطلاعاتی ندارم. می‌توانید به من یاد بدهید؟"
        ]
        
        return random.choice(responses)
    
    def learn_from_user(self, question, user_answer):
        """یادگیری از کاربر"""
        self.save_learned(question, user_answer)
        return f"✅ یاد گرفتم! دفعه بعد می‌دانم چگونه به '{question}' پاسخ دهم."
    
    def set_user_name(self, name):
        """تنظیم نام کاربر"""
        self.user_name = name
        return f"✅ خوشحالم که شما را می‌شناسم، {name}!"
    
    def show_stats(self):
        """نمایش آمار"""
        print(f"\n📊 آمار این جلسه:")
        print(f"   🕐 شروع: {self.stats['session_start']}")
        print(f"   ❓ سوالات: {self.stats['questions_asked']}")
        print(f"   🎯 موضوعات: {len(self.stats['topics_covered'])}")
        print(f"   ❓ سوالات ناشناخته: {len(self.stats['unknown_questions'])}")
        
        if self.user_name:
            print(f"   👤 کاربر: {self.user_name}")
    
    def show_help(self):
        """نمایش راهنما"""
        print("\n📋 راهنمای دستورات:")
        print("   [هر سوالی] - پرسش معمولی")
        print("   'اسم من [نام]' - تنظیم نام شما")
        print("   'یاد بگیر [سوال]|[پاسخ]' - آموزش پاسخ جدید")
        print("   'آمار' - نمایش آمار")
        print("   'موضوعات' - لیست موضوعات")
        print("   'خروج' - پایان گفتگو")
    
    def show_topics(self):
        """نمایش موضوعات موجود"""
        print("\n📚 موضوعات موجود:")
        for topic in self.knowledge.keys():
            print(f"   • {topic}")
        
        if self.learned:
            print("\n🎓 موضوعات آموخته شده:")
            for i, (q, a) in enumerate(list(self.learned.items())[:5], 1):
                print(f"   {i}. {q[:30]}...")

    def run(self):
        """اجرای سیستم"""
        print("🧠 natiq-ultimate - نسخه هوشمند")
        print("=" * 70)
        print("ویژگی‌های جدید:")
        print("• یادگیری از کاربر")
        print("• شناخت کاربر")
        print("• پاسخ‌های شخصی‌سازی شده")
        print("• ذخیره دانش آموخته شده")
        print("=" * 70)
        
        self.show_help()
        print("\n" + "-" * 70)
        
        while True:
            try:
                print("\n" + "─" * 40)
                user_input = input("🧑 شما: ").strip()
                
                if not user_input:
                    continue
                
                # دستورات ویژه
                if user_input.lower() in ["خروج", "exit", "quit"]:
                    print("👋 خداحافظ! امیدوارم مفید بوده باشم.")
                    self.show_stats()
                    break
                
                elif user_input.lower() == "آمار":
                    self.show_stats()
                    continue
                
                elif user_input.lower() == "موضوعات":
                    self.show_topics()
                    continue
                
                elif user_input.lower() == "راهنما":
                    self.show_help()
                    continue
                
                # تنظیم نام کاربر
                elif user_input.startswith("اسم من "):
                    name = user_input[7:].strip()
                    response = self.set_user_name(name)
                    print(f"🤖 {response}")
                    continue
                
                # یادگیری دستی
                elif user_input.startswith("یاد بگیر "):
                    parts = user_input[9:].split("|")
                    if len(parts) == 2:
                        question, answer = parts[0].strip(), parts[1].strip()
                        response = self.learn_from_user(question, answer)
                        print(f"🤖 {response}")
                    else:
                        print("⚠️ فرمت صحیح: 'یاد بگیر سوال|پاسخ'")
                    continue
                
                # پردازش سوال معمولی
                self.stats["questions_asked"] += 1
                
                # تحلیل سوال
                analysis = self.analyze_question(user_input)
                self.stats["topics_covered"].add(analysis["topic"])
                
                print(f"🤔 نوع: {analysis['type']} | موضوع: {analysis['topic']}")
                
                # تولید پاسخ
                answer = self.generate_answer(user_input, analysis)
                print(f"🤖 natiq: {answer}")
                
                # ذخیره گفتگو
                self.save_conversation(user_input, answer)
                
                # اگر سوال ناشناخته بود، پیشنهاد یادگیری
                if "یاد بگیر" in answer or "پاسخی" in answer:
                    print("💡 می‌توانید با 'یاد بگیر سوال|پاسخ' به من آموزش دهید.")
                
            except KeyboardInterrupt:
                print("\n\n👋 خروج از برنامه...")
                self.show_stats()
                break
            except Exception as e:
                print(f"❌ خطا: {e}")

def main():
    # ایجاد سیستم و اجرا
    natiq = NatiqSmart()
    natiq.run()

if __name__ == "__main__":
    main()
