"""
هسته هوشمند natiq-ultimate - نسخه نهایی
"""

import json
import re
import os
from datetime import datetime
from pathlib import Path

class NatiqSmart:
    def __init__(self):
        self.user_name = "کاربر"
        self.stats = {
            "questions_asked": 0,
            "topics_covered": set(),
            "session_start": datetime.now().isoformat()
        }
        
        # ایجاد پوشه‌های داده
        self.data_dir = Path("data")
        self.knowledge_dir = self.data_dir / "knowledge"
        self.conv_dir = self.data_dir / "conversations"
        
        for dir_path in [self.data_dir, self.knowledge_dir, self.conv_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # بارگیری دانش پایه
        self.knowledge = self.load_knowledge()
        
    def load_knowledge(self):
        """بارگیری دانش ذخیره شده"""
        knowledge_file = self.knowledge_dir / "base_knowledge.json"
        
        # دانش پایه
        base_knowledge = {
            "هوش مصنوعی": "هوش مصنوعی شاخه‌ای از علوم کامپیوتر است که به ساخت ماشین‌های هوشمند می‌پردازد.",
            "پایتون": "پایتون یک زبان برنامه‌نویسی سطح بالا و همه‌منظوره است.",
            "برنامه‌نویسی": "برنامه‌نویسی هنر نوشتن دستوراتی است که کامپیوتر آن‌ها را اجرا می‌کند.",
            "یادگیری ماشین": "یادگیری ماشین زیرشاخه‌ای از هوش مصنوعی است که به کامپیوترها توانایی یادگیری از داده را می‌دهد.",
            "natiq": "natiq-ultimate یک پروژه هوش مصنوعی فارسی است که می‌تواند یاد بگیرد و پاسخ دهد."
        }
        
        # تلاش برای بارگیری از فایل
        try:
            if knowledge_file.exists():
                with open(knowledge_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    return {**base_knowledge, **loaded}
        except:
            pass
        
        return base_knowledge
    
    def save_knowledge(self):
        """ذخیره دانش"""
        try:
            knowledge_file = self.knowledge_dir / "base_knowledge.json"
            with open(knowledge_file, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge, f, ensure_ascii=False, indent=2)
        except:
            pass  # در Vercel ممکن است نوشتن فایل امکان‌پذیر نباشد
    
    def analyze_question(self, question):
        """تحلیل سوال"""
        question_lower = question.lower()
        
        # الگوهای شناسایی
        patterns = {
            "greeting": [r"سلام", r"درود", r"علیک", r"hello", r"hi"],
            "name_query": [r"اسمت چیه", r"تو کیه", r"نام تو", r"کی هستی"],
            "name_set": [r"اسم من (\w+)", r"من (\w+) هستم", r"نام من (\w+)"],
            "learn": [r"یاد بگیر (.+)\|(.+)", r"آموزش بده (.+) جوابش (.+)"],
            "stats": [r"آمار", r"stat", r"تعداد سوال"],
            "topics": [r"موضوعات", r"topics", r"چه چیزهایی"]
        }
        
        for pattern_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, question_lower, re.IGNORECASE):
                    return {"type": pattern_type, "topic": pattern_type}
        
        # شناسایی موضوع از دانش
        for topic in self.knowledge.keys():
            if topic.lower() in question_lower:
                return {"type": "knowledge_query", "topic": topic}
        
        return {"type": "general", "topic": "عمومی"}
    
    def generate_answer(self, question, analysis):
        """تولید پاسخ"""
        self.stats["questions_asked"] += 1
        
        # پردازش بر اساس نوع
        if analysis["type"] == "greeting":
            return f"سلام {self.user_name}! خوش آمدید. چطور می‌تونم کمک کنم؟"
        
        elif analysis["type"] == "name_query":
            return f"من natiq-ultimate هستم، دستیار هوشمند فارسی شما! 🤖"
        
        elif analysis["type"] == "name_set":
            match = re.search(r"اسم من (\w+)", question)
            if match:
                self.user_name = match.group(1)
                return f"سلام {self.user_name}! خوشحالم که شما را می‌شناسم. 😊"
        
        elif analysis["type"] == "learn":
            match = re.search(r"یاد بگیر (.+)\|(.+)", question)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                self.knowledge[key] = value
                self.save_knowledge()
                self.stats["topics_covered"].add(key)
                return f"✅ موفقیت! '{key}' را یاد گرفتم:\n{value}"
        
        elif analysis["type"] == "stats":
            return f"📊 آمار جلسه:\n• سوالات: {self.stats['questions_asked']}\n• موضوعات: {len(self.stats['topics_covered'])}\n• کاربر: {self.user_name}"
        
        elif analysis["type"] == "topics":
            topics = list(self.knowledge.keys())[:10]
            return f"📚 موضوعات موجود ({len(topics)} مورد):\n" + "\n".join([f"• {topic}" for topic in topics])
        
        elif analysis["type"] == "knowledge_query":
            topic = analysis["topic"]
            if topic in self.knowledge:
                self.stats["topics_covered"].add(topic)
                return self.knowledge[topic]
        
        # پاسخ پیش‌فرض
        responses = [
            f"متوجه سوال شما شدم. در حال حاضر اطلاعات کافی درباره '{question}' ندارم.",
            f"علاقه‌مندم در این مورد یاد بگیرم! می‌توانید با فرمت 'یاد بگیر {question}|پاسخ' به من آموزش دهید.",
            f"سوال جالبی پرسیدید. من natiq-ultimate هستم و در حال یادگیری هستم.",
            f"پاسخ این سوال را نمی‌دانم، اما می‌توانم چیزهای دیگری به شما یاد بدهم!"
        ]
        
        return responses[self.stats["questions_asked"] % len(responses)]
    
    def save_conversation(self, question, answer):
        """ذخیره گفتگو"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            conv_file = self.conv_dir / f"conversation_{timestamp}.json"
            
            conversation = {
                "timestamp": datetime.now().isoformat(),
                "question": question,
                "answer": answer,
                "user": self.user_name,
                "environment": os.getenv("VERCEL_ENV", "local")
            }
            
            with open(conv_file, 'w', encoding='utf-8') as f:
                json.dump(conversation, f, ensure_ascii=False, indent=2)
        except:
            pass  # در Vercel ممکن است نوشتن فایل امکان‌پذیر نباشد

