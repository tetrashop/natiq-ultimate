"""
نسخه ساده شده natiq_smart برای تست سریع
"""

import json
from datetime import datetime

class NatiqSmart:
    def __init__(self):
        self.user_name = "کاربر"
        self.stats = {
            "questions_asked": 0,
            "topics_covered": set(),
            "session_start": datetime.now().isoformat()
        }
        
    def analyze_question(self, question):
        """تحلیل ساده سوال"""
        question_lower = question.lower()
        
        if "سلام" in question_lower:
            return {"type": "greeting", "topic": "سلام"}
        elif "اسم" in question_lower and ("چیه" in question_lower or "تو" in question_lower):
            return {"type": "name_query", "topic": "نام"}
        elif "اسم من" in question_lower:
            return {"type": "name_set", "topic": "نام"}
        elif "یاد بگیر" in question_lower:
            return {"type": "learn", "topic": "یادگیری"}
        elif "آمار" in question_lower:
            return {"type": "stats", "topic": "آمار"}
        else:
            return {"type": "general", "topic": "عمومی"}
    
    def generate_answer(self, question, analysis):
        """تولید پاسخ ساده"""
        self.stats["questions_asked"] += 1
        
        responses = {
            "greeting": f"سلام {self.user_name}! خوش آمدید. چطور می‌تونم کمک کنم؟",
            "name_query": "من natiq-ultimate هستم، دستیار هوشمند فارسی شما!",
            "name_set": f"سلام {self.user_name}! خوشحالم که شما رو می‌شناسم.",
            "learn": "متوجه شدم! می‌خواهید چیزی یادم بدید. برای آموزش از فرمت 'یاد بگیر سوال|پاسخ' استفاده کنید.",
            "stats": f"📊 آمار فعلی:\nسوالات: {self.stats['questions_asked']}\nکاربر: {self.user_name}",
            "general": "متوجه سوال شما شدم. من natiq-ultimate هستم و در حال یادگیری هستم!"
        }
        
        return responses.get(analysis["type"], "پاسخ پیش‌فرض")
    
    def save_conversation(self, question, answer):
        """ذخیره گفتگو"""
        pass

# ایجاد نمونه global
natiq_instance = NatiqSmart()
