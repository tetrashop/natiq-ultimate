# ~/natiq-ultimate/api/math_tutor.py
import json

class MathTutor:
    """مربی ریاضی هوشمند"""
    
    def __init__(self):
        self.curriculum = {
            "دبیرستان": {
                "جبر": ["معادله درجه دوم", "نمودار تابع", "لگاریتم"],
                "هندسه": ["قضیه فیثاغورث", "تشابه مثلث", "دایره"],
                "حسابان": ["مشتق", "انتگرال", "حد"]
            },
            "دانشگاه": {
                "جبر خطی": ["ماتریس", "دترمینان", "فضای برداری"],
                "آنالیز": ["سری", "حد و پیوستگی", "مشتق جزئی"],
                "آمار": ["توزیع نرمال", "رگرسیون", "احتمال"]
            }
        }
    
    def get_tutorial(self, topic: str, level: str = "دبیرستان"):
        """دریافت آموزش برای موضوع"""
        if level in self.curriculum and topic in self.curriculum[level]:
            return {
                "topic": topic,
                "level": level,
                "content": self._generate_content(topic, level),
                "examples": self._generate_examples(topic),
                "exercises": self._generate_exercises(topic)
            }
        return {"error": "موضوع پشتیبانی نمی‌شود"}
    
    def _generate_content(self, topic, level):
        """تولید محتوای آموزشی"""
        contents = {
            "معادله درجه دوم": """
            معادله درجه دوم به فرم ax² + bx + c = 0 است.
            فرمول حل: x = [-b ± √(b² - 4ac)] / 2a
            ممیز: Δ = b² - 4ac
            - اگر Δ > 0: دو جواب حقیقی
            - اگر Δ = 0: یک جواب حقیقی
            - اگر Δ < 0: دو جواب موهومی
            """
        }
        return contents.get(topic, "محتوای آموزشی در دست تهیه است.")
