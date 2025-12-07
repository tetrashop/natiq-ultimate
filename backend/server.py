#!/usr/bin/env python3
"""
natiq-ultimate - هوش مصنوعی فارسی پیشرفته
نسخه 3.0: با قابلیت‌های تشخیص پیشرفته و پاسخ‌های هوشمند
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import os
from datetime import datetime
import json
import random

app = FastAPI(
    title="natiq-ultimate",
    description="هوش مصنوعی فارسی پیشرفته با قابلیت‌های متنوع",
    version="3.0.0"
)

# CORS برای Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# کلاس هوش مصنوعی پیشرفته
class NatiqAdvancedAI:
    def __init__(self):
        self.user_name = "کاربر"
        self.stats = {
            "questions_asked": 0,
            "topics_covered": [],
            "last_interaction": datetime.now().isoformat()
        }
        self.knowledge_base = self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """پایگاه دانش فارسی"""
        return {
            "greetings": [
                "سلام! خوش آمدید. من natiq-ultimate هستم، دستیار هوشمند فارسی شما. 🤖",
                "درود! خوشحالم که شما را می‌بینم. چطور می‌توانم کمک کنم؟",
                "سلام عزیز! آماده‌ام به سوالات شما پاسخ دهم.",
                "سلام و وقت بخیر! من اینجام تا به شما کمک کنم."
            ],
            "farewells": [
                "خداحافظ! موفق باشید. 😊",
                "به امید دیدار مجدد!",
                "خدانگهدار! اگر سوال دیگری دارید، در خدمتم.",
                "با آرزوی بهترین‌ها برای شما! خداحافظ."
            ],
            "name": [
                "من natiq-ultimate هستم، یک دستیار هوش مصنوعی فارسی که توسط تیمی از توسعه‌دهندگان ایرانی ایجاد شده‌ام.",
                "اسم من natiq-ultimate است! در فارسی به معنای 'گویای نهایی' هستم.",
                "من natiq-ultimate نام دارم، نسخه پیشرفته هوش مصنوعی فارسی.",
                "به من natiq-ultimate می‌گویند. مأموریت من کمک به کاربران فارسی‌زبان است."
            ],
            "creator": [
                "من توسط تیمی از توسعه‌دهندگان ایرانی علاقه‌مند به هوش مصنوعی ایجاد شده‌ام.",
                "توسعه‌دهندگان ایرانی من را با عشق به زبان فارسی و تکنولوژی ساخته‌اند.",
                "یک تیم برنامه‌نویس ایرانی من را طراحی کرده تا به جامعه فارسی‌زبان خدمت کنم.",
                "سازنده‌های من عاشقان تکنولوژی و زبان فارسی هستند!"
            ],
            "capabilities": [
                "من می‌توانم: به سوالات فارسی پاسخ دهم، تحلیل متن انجام دهم، اطلاعات ارائه دهم، در گفتگو همراهیتان کنم و یادگیری مداوم دارم!",
                "قابلیت‌های من شامل: پردازش زبان فارسی، پاسخ به سوالات متداول، ارائه اطلاعات، گفتگوی تعاملی و پشتیبانی از کاربران است.",
                "می‌توانم در موضوعات مختلف با شما گفتگو کنم، سوالات شما را تحلیل کنم و پاسخ‌های مفید ارائه دهم.",
                "به عنوان یک دستیار فارسی، می‌توانم کمک‌های متنوعی ارائه دهم: از پاسخ به سوالات ساده تا تحلیل موضوعات پیچیده."
            ],
            "nlp_info": [
                "🔹 **آخرین پست صفحه NLP**: شماره 206\n📅 تاریخ: به‌زودی منتشر می‌شود\n📝 موضوع: پردازش زبان طبیعی پیشرفته\n✅ وضعیت: آماده انتشار\n\nاین پست جامع‌ترین مطلب در حوزه NLP فارسی خواهد بود!",
                "در مورد صفحه NLP: آخرین پست با شماره 206 در حال آماده‌سازی است و به زودی منتشر می‌شود.",
                "پست شماره 206 صفحه NLP در دست تهیه است و حاوی مطالب پیشرفته‌ای در مورد پردازش زبان طبیعی خواهد بود.",
                "آخرین به‌روزرسانی صفحه NLP: پست شماره 206 در مراحل نهایی است و به محض آماده شدن منتشر خواهد شد."
            ],
            "learning": [
                "بله! من دائماً در حال یادگیری هستم. هر گفتگو به من کمک می‌کند بهتر شوم.",
                "قطعاً! سیستم من بر پایه یادگیری مداوم طراحی شده است.",
                "آره، با هر تعاملی چیزهای جدیدی یاد می‌گیرم.",
                "یادگیری بخش جدایی‌ناپذیر من است. هر روز بهتر از دیروز می‌شوم!"
            ],
            "jokes": [
                "چرا کامپیوتر نمی‌تواند دروغ بگوید؟ چون همیشه حقیقت را بایت می‌کند! 😄",
                "دو تا صفر با هم دعوا کردن... هر دو باختند! 🤭",
                "الگوریتمی وارد کافه شد و گفت: 'من مرتب می‌شوم!' 🫢",
                "چرا برنامه‌نویس از طبیعت بدش می‌آمد؟ چون باگ داشت! 🐛"
            ],
            "technology": [
                "فناوری‌های به کار رفته در من: Python, FastAPI, Machine Learning, NLP",
                "من با پایتون و فریمورک FastAPI ساخته شده‌ام و از الگوریتم‌های پردازش زبان طبیعی استفاده می‌کنم.",
                "زیرساخت من شامل پایتون، یادگیری ماشین و APIهای مدرن است.",
                "تکنولوژی‌های اصلی من: هوش مصنوعی، پردازش زبان فارسی، و معماری مبتنی بر API."
            ],
            "help": [
                "من می‌توانم در زمینه‌های زیر کمک کنم:\n• پاسخ به سوالات عمومی\n• اطلاعات تکنولوژی\n• گفتگوی دوستانه\n• موضوعات علمی\n• و هر موضوع دیگری که بخواهید!",
                "برای کمک می‌توانید:\n1. سوال خود را بپرسید\n2. از دکمه‌های سریع استفاده کنید\n3. موضوع مورد نظر را مشخص کنید\n\nمن سعی می‌کنم بهترین پاسخ را بدهم.",
                "کمک رسانی تخصص من است! فقط کافیست بپرسید.",
                "در خدمتم! لطفاً سوال یا درخواست خود را مطرح کنید."
            ]
        }
    
    def analyze_question(self, question):
        """تحلیل پیشرفته سوال با پوشش گسترده‌تر"""
        question_lower = question.lower().strip()
        
        # بررسی سلام و احوالپرسی
        greeting_keywords = ['سلام', 'درود', 'صبخ', 'عصر', 'وقت', 'hey', 'hello']
        if any(keyword in question_lower for keyword in greeting_keywords):
            return {"type": "greeting", "topic": "احوالپرسی", "confidence": 0.95}
        
        # بررسی خداحافظی
        farewell_keywords = ['خداحافظ', 'بای', 'bye', 'خدانگهدار', 'متشکرم']
        if any(keyword in question_lower for keyword in farewell_keywords):
            return {"type": "farewell", "topic": "خداحافظی", "confidence": 0.90}
        
        # بررسی نام
        name_keywords = ['اسم', 'نام', 'کیستی', 'چه اسمی', 'نام تو', 'تو کی']
        if any(keyword in question_lower for keyword in name_keywords):
            return {"type": "name", "topic": "معرفی", "confidence": 0.92}
        
        # بررسی سازنده
        creator_keywords = ['سازنده', 'چه کسی', 'چه کسی ساخت', 'چه کسی ایجاد', 'چه کسی نوشت']
        if any(keyword in question_lower for keyword in creator_keywords):
            return {"type": "creator", "topic": "سازنده", "confidence": 0.88}
        
        # بررسی قابلیت‌ها
        capability_keywords = ['چه کار', 'چه کاری', 'چه می‌توانی', 'قابلیت', 'توانایی', 'کارایی']
        if any(keyword in question_lower for keyword in capability_keywords):
            return {"type": "capabilities", "topic": "قابلیت‌ها", "confidence": 0.85}
        
        # بررسی NLP و آخرین پست
        nlp_keywords = ['nlp', 'آخرین پست', 'پست ۲۰۶', 'پست 206', 'صفحه nlp', 'پردازش زبان']
        if any(keyword in question_lower for keyword in nlp_keywords):
            return {"type": "nlp_info", "topic": "NLP", "confidence": 0.96}
        
        # بررسی یادگیری
        learning_keywords = ['یاد می‌گیری', 'یادگیری', 'بهتر می‌شوی', 'پیشرفت', 'یاد گرفتی']
        if any(keyword in question_lower for keyword in learning_keywords):
            return {"type": "learning", "topic": "یادگیری", "confidence": 0.87}
        
        # بررسی جوک و طنز
        joke_keywords = ['جوک', 'طنز', 'خنده', 'مضحک', 'بامزه', 'لطیفه']
        if any(keyword in question_lower for keyword in joke_keywords):
            return {"type": "joke", "topic": "طنز", "confidence": 0.82}
        
        # بررسی تکنولوژی
        tech_keywords = ['تکنولوژی', 'فناوری', 'چگونه کار', 'چطور کار', 'ساختار', 'معماری']
        if any(keyword in question_lower for keyword in tech_keywords):
            return {"type": "technology", "topic": "تکنولوژی", "confidence": 0.84}
        
        # بررسی کمک
        help_keywords = ['کمک', 'راهنمایی', 'کمک کن', 'راهنمایی کن', 'کمک می‌کنی']
        if any(keyword in question_lower for keyword in help_keywords):
            return {"type": "help", "topic": "کمک", "confidence": 0.89}
        
        # بررسی آمار
        stats_keywords = ['آمار', 'stat', 'تعداد', 'چندتا', 'چند تا پرسید']
        if any(keyword in question_lower for keyword in stats_keywords):
            return {"type": "stats", "topic": "آمار", "confidence": 0.91}
        
        # در غیر این صورت، تحلیل عمیق‌تر
        return self.deep_analysis(question_lower)
    
    def deep_analysis(self, question):
        """تحلیل عمیق‌تر برای سوالات پیچیده"""
        words = question.split()
        
        # تشخیص سوالات Wh
        wh_words = ['چه', 'چرا', 'چگونه', 'چطور', 'کی', 'کجا', 'چه زمانی', 'چند']
        wh_count = sum(1 for word in words if word in wh_words)
        
        if wh_count > 0:
            if 'چرا' in question:
                return {"type": "why_question", "topic": "علت‌یابی", "confidence": 0.80}
            elif 'چگونه' in question or 'چطور' in question:
                return {"type": "how_question", "topic": "روش‌شناسی", "confidence": 0.82}
            elif 'چه' in question:
                return {"type": "what_question", "topic": "توضیح", "confidence": 0.85}
        
        # تشخیص سوالات بله/خیر
        if question.endswith('؟') and len(words) < 8:
            return {"type": "yesno_question", "topic": "تأیید/رد", "confidence": 0.75}
        
        # تشخیص درخواست
        request_keywords = ['می‌خواهم', 'لطفا', 'لطفاً', 'می‌توانی', 'میشه']
        if any(keyword in question for keyword in request_keywords):
            return {"type": "request", "topic": "درخواست", "confidence": 0.78}
        
        # پیش‌فرض
        return {"type": "general", "topic": "عمومی", "confidence": 0.70}
    
    def generate_answer(self, question, analysis):
        """تولید پاسخ هوشمند بر اساس تحلیل"""
        self.stats["questions_asked"] += 1
        self.stats["topics_covered"].append(analysis["topic"])
        self.stats["last_interaction"] = datetime.now().isoformat()
        
        # انتخاب تصادفی از لیست پاسخ‌های مناسب
        response_type = analysis["type"]
        
        if response_type in self.knowledge_base:
            response = random.choice(self.knowledge_base[response_type])
            return response
        
        # پاسخ‌های پیش‌فرض برای انواع سوالات
        responses = {
            "why_question": f"سوال خوبی پرسیدید! در مورد '{question}' باید بگویم که...",
            "how_question": f"برای '{question}'، مراحل زیر را پیشنهاد می‌کنم:\n1. ...\n2. ...\n3. ...",
            "what_question": f"'{question}' به این معناست که...",
            "yesno_question": f"در پاسخ به '{question}'، می‌توان گفت که احتمالاً بله!",
            "request": f"درخواست شما برای '{question}' دریافت شد. سعی می‌کنم کمک کنم!",
            "general": self.generate_educated_response(question),
            "stats": f"📊 **آمار تعامل**:\n• سوالات پاسخ داده: {self.stats['questions_asked']}\n• موضوعات پوشش داده شده: {', '.join(set(self.stats['topics_covered']))}\n• آخرین تعامل: {self.stats['last_interaction']}"
        }
        
        return responses.get(response_type, self.generate_educated_response(question))
    
    def generate_educated_response(self, question):
        """تولید پاسخ آموزنده برای سوالات عمومی"""
        educated_responses = [
            f"سوال جالبی پرسیدید: '{question}'. در این مورد باید بگویم که...",
            f"در مورد '{question}'، اطلاعات مفیدی می‌توانم ارائه دهم. آیا می‌خواهید بیشتر توضیح دهم؟",
            f"'{question}' - موضوع مهمی است! می‌توانم در این زمینه کمک کنم.",
            f"از سوال شما متشکرم! '{question}' را تحلیل کردم و می‌توانم راهنمایی کنم.",
            f"در مورد '{question}'، چند نکته کلیدی وجود دارد که باید بدانید..."
        ]
        return random.choice(educated_responses)

# صفحه اصلی با HTML کامل
@app.get("/")
async def root():
    html_content = """
    <!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🤖 natiq-ultimate v3.0 | هوش مصنوعی فارسی پیشرفته</title>
        <style>
            /* Reset */
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Vazirmatn', 'Segoe UI', Tahoma, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
                line-height: 1.6;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                min-height: 100vh;
                box-shadow: 0 0 40px rgba(0,0,0,0.1);
            }
            
            /* Header */
            .header {
                background: linear-gradient(90deg, #4f46e5, #7c3aed);
                color: white;
                padding: 20px 30px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
            }
            
            .logo {
                display: flex;
                align-items: center;
                gap: 15px;
            }
            
            .logo i {
                font-size: 2.5em;
                animation: float 3s ease-in-out infinite;
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }
            
            .logo h1 {
                font-size: 1.8em;
                font-weight: 700;
            }
            
            .version {
                background: rgba(255,255,255,0.2);
                padding: 5px 15px;
                border-radius: 15px;
                font-size: 0.9em;
                font-weight: bold;
            }
            
            .status {
                display: flex;
                align-items: center;
                gap: 10px;
                background: rgba(255,255,255,0.1);
                padding: 8px 20px;
                border-radius: 20px;
            }
            
            .status-dot {
                width: 10px;
                height: 10px;
                background: #4ade80;
                border-radius: 50%;
                animation: blink 1.5s infinite;
            }
            
            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.3; }
            }
            
            /* Main Content */
            .main-content {
                display: flex;
                min-height: 70vh;
            }
            
            .chat-area {
                flex: 1;
                padding: 30px;
                background: #f8fafc;
                display: flex;
                flex-direction: column;
            }
            
            .messages {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
                background: white;
                border-radius: 15px;
                box-shadow: inset 0 0 10px rgba(0,0,0,0.05);
                margin-bottom: 25px;
                max-height: 60vh;
            }
            
            .message {
                margin: 15px 0;
                padding: 15px 20px;
                border-radius: 15px;
                max-width: 85%;
                animation: slideIn 0.3s ease;
            }
            
            @keyframes slideIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .bot-message {
                background: linear-gradient(135deg, #e3f2fd, #bbdefb);
                margin-right: auto;
                border-top-right-radius: 5px;
                border-right: 4px solid #2196f3;
            }
            
            .user-message {
                background: linear-gradient(135deg, #4f46e5, #7c3aed);
                color: white;
                margin-left: auto;
                border-top-left-radius: 5px;
                border-left: 4px solid #3730a3;
            }
            
            .error-message {
                background: #fee2e2;
                border-right: 4px solid #dc2626;
                color: #7f1d1d;
            }
            
            .info-message {
                background: #f0f9ff;
                border-right: 4px solid #0ea5e9;
                color: #0369a1;
            }
            
            /* Input Area */
            .input-area {
                background: white;
                padding: 20px;
                border-top: 1px solid #e5e7eb;
            }
            
            .input-group {
                display: flex;
                gap: 12px;
                margin-bottom: 15px;
            }
            
            #messageInput {
                flex: 1;
                padding: 15px 20px;
                border: 2px solid #e5e7eb;
                border-radius: 25px;
                font-size: 1em;
                font-family: inherit;
                transition: all 0.3s;
            }
            
            #messageInput:focus {
                outline: none;
                border-color: #4f46e5;
                box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
            }
            
            #sendButton {
                width: 60px;
                background: linear-gradient(45deg, #4f46e5, #7c3aed);
                color: white;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 1.2em;
                transition: all 0.3s;
            }
            
            #sendButton:hover {
                transform: scale(1.05);
                box-shadow: 0 5px 20px rgba(79, 70, 229, 0.3);
            }
            
            .quick-buttons {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .quick-btn {
                padding: 10px 20px;
                background: #f3f4f6;
                border: 1px solid #e5e7eb;
                border-radius: 15px;
                cursor: pointer;
                transition: all 0.3s;
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 0.9em;
                flex: 1;
                min-width: 150px;
                justify-content: center;
            }
            
            .quick-btn:hover {
                background: #e5e7eb;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            
            .quick-btn.nlp {
                background: linear-gradient(45deg, #8b5cf6, #7c3aed);
                color: white;
                border: none;
            }
            
            /* Sidebar */
            .sidebar {
                width: 320px;
                background: #f9fafb;
                border-left: 1px solid #e5e7eb;
                padding: 25px 20px;
                overflow-y: auto;
            }
            
            .sidebar-section {
                margin-bottom: 25px;
                padding-bottom: 20px;
                border-bottom: 1px solid #e5e7eb;
            }
            
            .sidebar-section h3 {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 15px;
                color: #374151;
                font-size: 1.1em;
            }
            
            /* Welcome Message */
            .welcome {
                background: linear-gradient(135deg, #e3f2fd, #bbdefb);
                padding: 25px;
                border-radius: 15px;
                margin-bottom: 20px;
                border-right: 5px solid #2196f3;
            }
            
            .welcome h2 {
                color: #1565c0;
                margin-bottom: 12px;
                font-size: 1.4em;
            }
            
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }
            
            .feature {
                background: white;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                transition: transform 0.3s;
            }
            
            .feature:hover {
                transform: translateY(-5px);
            }
            
            .feature i {
                font-size: 2em;
                color: #4f46e5;
                margin-bottom: 10px;
            }
            
            /* Responsive */
            @media (max-width: 1024px) {
                .main-content {
                    flex-direction: column;
                }
                
                .sidebar {
                    width: 100%;
                    border-left: none;
                    border-top: 1px solid #e5e7eb;
                }
            }
            
            @media (max-width: 768px) {
                .container {
                    margin: 0;
                }
                
                .header {
                    padding: 15px;
                    flex-direction: column;
                    gap: 15px;
                    text-align: center;
                }
                
                .logo {
                    flex-direction: column;
                    gap: 10px;
                }
                
                .message {
                    max-width: 95%;
                }
                
                .input-group {
                    flex-direction: column;
                }
                
                #sendButton {
                    width: 100%;
                    height: 50px;
                }
                
                .quick-btn {
                    min-width: 120px;
                }
                
                .features {
                    grid-template-columns: 1fr;
                }
            }
            
            /* Message time */
            .message-time {
                font-size: 0.8em;
                opacity: 0.7;
                margin-top: 5px;
                text-align: left;
            }
            
            .user-message .message-time {
                text-align: right;
            }
            
            /* Stats display */
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
                margin-top: 10px;
            }
            
            .stat-item {
                background: white;
                padding: 10px;
                border-radius: 8px;
                text-align: center;
                border: 1px solid #e5e7eb;
            }
            
            .stat-value {
                font-size: 1.5em;
                font-weight: bold;
                color: #4f46e5;
            }
        </style>
        
        <!-- Font Awesome -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        
        <!-- Google Fonts -->
        <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        
        <script>
            class NatiqApp {
                constructor() {
                    this.sessionId = 'natiq_' + Date.now();
                    this.baseUrl = window.location.origin;
                    this.messageCount = 0;
                    this.init();
                }
                
                init() {
                    console.log('🚀 natiq-ultimate v3.0 شروع شد');
                    this.setupEventListeners();
                    this.updateStatus('✅ متصل به سرور');
                    
                    // نمایش تاریخ و زمان
                    this.updateDateTime();
                    setInterval(() => this.updateDateTime(), 60000);
                }
                
                setupEventListeners() {
                    const sendBtn = document.getElementById('sendButton');
                    const messageInput = document.getElementById('messageInput');
                    
                    sendBtn.addEventListener('click', () => this.sendMessage());
                    
                    messageInput.addEventListener('keypress', (e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault();
                            this.sendMessage();
                        }
                    });
                    
                    // دکمه‌های سریع
                    document.querySelectorAll('.quick-btn').forEach(btn => {
                        btn.addEventListener('click', (e) => {
                            const text = e.target.getAttribute('data-question') || 
                                       e.target.closest('.quick-btn').getAttribute('data-question');
                            if (text) {
                                messageInput.value = text;
                                this.sendMessage();
                            }
                        });
                    });
                }
                
                updateDateTime() {
                    const now = new Date();
                    const options = {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                    };
                    const dateStr = now.toLocaleDateString('fa-IR', options);
                    document.getElementById('currentDateTime').textContent = dateStr;
                }
                
                updateStatus(message) {
                    const statusText = document.getElementById('statusText');
                    if (statusText) {
                        statusText.textContent = message;
                    }
                }
                
                async sendMessage() {
                    const messageInput = document.getElementById('messageInput');
                    const message = messageInput.value.trim();
                    
                    if (!message) return;
                    
                    // نمایش پیام کاربر
                    this.addMessage(message, 'user');
                    messageInput.value = '';
                    this.messageCount++;
                    
                    // نمایش تایپینگ
                    this.showTyping();
                    
                    try {
                        const response = await fetch(this.baseUrl + '/api/chat/' + this.sessionId, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ message: message })
                        });
                        
                        if (!response.ok) {
                            throw new Error(`خطای HTTP: ${response.status}`);
                        }
                        
                        const data = await response.json();
                        
                        this.hideTyping();
                        this.addMessage(data.answer, 'bot');
                        this.updateStatus('✅ پاسخ دریافت شد');
                        
                        // بروزرسانی آمار
                        this.updateStats();
                        
                    } catch (error) {
                        this.hideTyping();
                        console.error('❌ خطا:', error);
                        
                        this.addMessage('⚠️ خطا در ارتباط با سرور. لطفاً دوباره تلاش کنید.', 'error');
                        this.updateStatus('❌ خطا در ارتباط');
                    }
                }
                
                addMessage(text, type) {
                    const messagesDiv = document.getElementById('messages');
                    const time = new Date().toLocaleTimeString('fa-IR', {
                        hour: '2-digit',
                        minute: '2-digit'
                    });
                    
                    const messageDiv = document.createElement('div');
                    messageDiv.className = `message ${type === 'user' ? 'user-message' : type === 'error' ? 'error-message' : 'bot-message'}`;
                    
                    const icon = type === 'user' ? '👤' : 
                                 type === 'error' ? '⚠️' : '🤖';
                    
                    messageDiv.innerHTML = `
                        <div style="display: flex; align-items: flex-start; gap: 12px;">
                            <div style="font-size: 1.4em; flex-shrink: 0;">
                                ${icon}
                            </div>
                            <div style="flex: 1;">
                                <div style="white-space: pre-wrap;">${this.escapeHtml(text)}</div>
                                <div class="message-time">${time}</div>
                            </div>
                        </div>
                    `;
                    
                    messagesDiv.appendChild(messageDiv);
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }
                
                showTyping() {
                    const messagesDiv = document.getElementById('messages');
                    
                    const typingDiv = document.createElement('div');
                    typingDiv.className = 'message bot-message';
                    typingDiv.id = 'typingIndicator';
                    typingDiv.innerHTML = `
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <div>🤖</div>
                            <div style="display: flex; gap: 5px;">
                                <span style="animation: blink 1.4s infinite; color: #4f46e5;">●</span>
                                <span style="animation: blink 1.4s infinite 0.2s; color: #7c3aed;">●</span>
                                <span style="animation: blink 1.4s infinite 0.4s; color: #8b5cf6;">●</span>
                            </div>
                        </div>
                    `;
                    
                    messagesDiv.appendChild(typingDiv);
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }
                
                hideTyping() {
                    const typing = document.getElementById('typingIndicator');
                    if (typing) {
                        typing.remove();
                    }
                }
                
                updateStats() {
                    document.getElementById('messageCount').textContent = this.messageCount;
                    document.getElementById('sessionIdDisplay').textContent = this.sessionId;
                }
                
                escapeHtml(text) {
                    const div = document.createElement('div');
                    div.textContent = text;
                    return div.innerHTML;
                }
                
                // تست سلامت
                async testHealth() {
                    try {
                        const response = await fetch(this.baseUrl + '/api/health');
                        const data = await response.json();
                        return data;
                    } catch (error) {
                        return null;
                    }
                }
            }
            
            // راه‌اندازی اپ
            document.addEventListener('DOMContentLoaded', () => {
                window.natiqApp = new NatiqApp();
                document.getElementById('messageInput').focus();
                
                // تست خودکار سلامت
                setTimeout(async () => {
                    const health = await window.natiqApp.testHealth();
                    if (health) {
                        console.log('✅ سلامت سیستم:', health);
                    }
                }, 1000);
            });
        </script>
    </head>
    <body>
        <div class="container">
            <!-- هدر -->
            <header class="header">
                <div class="logo">
                    <i class="fas fa-robot"></i>
                    <div>
                        <h1>natiq-ultimate</h1>
                        <span class="version">نسخه ۳.۰</span>
                    </div>
                </div>
                <div class="status">
                    <span class="status-dot"></span>
                    <span id="statusText">در حال اتصال...</span>
                </div>
            </header>
            
            <!-- محتوای اصلی -->
            <div class="main-content">
                <!-- قسمت چت -->
                <div class="chat-area">
                    <div class="messages" id="messages">
                        <!-- پیام خوش‌آمدگویی -->
                        <div class="welcome">
                            <h2>🚀 به natiq-ultimate خوش آمدید!</h2>
                            <p>من یک دستیار هوش مصنوعی فارسی پیشرفته هستم که می‌توانم به سوالات متنوع شما پاسخ دهم.</p>
                            
                            <div class="features">
                                <div class="feature">
                                    <i class="fas fa-brain"></i>
                                    <h3>هوش پیشرفته</h3>
                                    <p>پردازش زبان طبیعی فارسی</p>
                                </div>
                                <div class="feature">
                                    <i class="fas fa-comments"></i>
                                    <h3>گفتگوی طبیعی</h3>
                                    <p>مکالمه روان و کاربردی</p>
                                </div>
                                <div class="feature">
                                    <i class="fas fa-bolt"></i>
                                    <h3>پاسخ سریع</h3>
                                    <p>واکنش آنی به درخواست‌ها</p>
                                </div>
                                <div class="feature">
                                    <i class="fas fa-graduation-cap"></i>
                                    <h3>یادگیری مداوم</h3>
                                    <p>بهبود مستقل عملکرد</p>
                                </div>
                            </div>
                            
                            <p><strong>💡 نکته:</strong> سوال خود را بنویسید یا از دکمه‌های زیر استفاده کنید.</p>
                        </div>
                    </div>
                    
                    <!-- ورودی -->
                    <div class="input-area">
                        <div class="input-group">
                            <input 
                                type="text" 
                                id="messageInput" 
                                placeholder="سوال یا درخواست خود را اینجا بنویسید..." 
                                autocomplete="off"
                                autofocus
                            >
                            <button id="sendButton">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                        
                        <div class="quick-buttons">
                            <button class="quick-btn" data-question="سلام">
                                <i class="fas fa-hand"></i> سلام
                            </button>
                            <button class="quick-btn nlp" data-question="آخرین پست صفحه nlp">
                                <i class="fas fa-file-alt"></i> پست ۲۰۶ NLP
                            </button>
                            <button class="quick-btn" data-question="اسم تو چیست؟">
                                <i class="fas fa-robot"></i> معرفی
                            </button>
                            <button class="quick-btn" data-question="چه کارهایی می‌توانی انجام دهی؟">
                                <i class="fas fa-list"></i> قابلیت‌ها
                            </button>
                            <button class="quick-btn" data-question="آمار این جلسه">
                                <i class="fas fa-chart-bar"></i> آمار
                            </button>
                            <button class="quick-btn" data-question="یک جوک بگو">
                                <i class="fas fa-laugh"></i> جوک
                            </button>
                            <button class="quick-btn" data-question="چگونه کار می‌کنی؟">
                                <i class="fas fa-cogs"></i> نحوه کار
                            </button>
                            <button class="quick-btn" data-question="چه کسی تو را ساخته است؟">
                                <i class="fas fa-code"></i> سازنده
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- سایدبار -->
                <div class="sidebar">
                    <div class="sidebar-section">
                        <h3><i class="fas fa-info-circle"></i> اطلاعات سیستم</h3>
                        <div class="stats-grid">
                            <div class="stat-item">
                                <div class="stat-value" id="messageCount">0</div>
                                <div>پیام‌ها</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">۳.۰</div>
                                <div>نسخه</div>
                            </div>
                        </div>
                        <p style="margin-top: 15px; font-size: 0.9em;">
                            <strong>🌐 محیط:</strong> Vercel<br>
                            <strong>🚀 وضعیت:</strong> فعال<br>
                            <strong>📅 زمان:</strong> <span id="currentDateTime">--</span><br>
                            <strong>🔗 شناسه:</strong> <span id="sessionIdDisplay">...</span>
                        </p>
                    </div>
                    
                    <div class="sidebar-section">
                        <h3><i class="fas fa-terminal"></i> عملیات سریع</h3>
                        <div>
                            <button onclick="testApi()" style="width:100%; padding:12px; background:#4f46e5; color:white; border:none; border-radius:8px; cursor:pointer; margin-bottom:10px; display:flex; align-items:center; justify-content:center; gap:8px;">
                                <i class="fas fa-heartbeat"></i> تست سلامت API
                            </button>
                            <button onclick="clearChat()" style="width:100%; padding:12px; background:#ef4444; color:white; border:none; border-radius:8px; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:8px;">
                                <i class="fas fa-trash"></i> پاک کردن چت
                            </button>
                            <button onclick="showNlpInfo()" style="width:100%; padding:12px; background:#8b5cf6; color:white; border:none; border-radius:8px; cursor:pointer; margin-top:10px; display:flex; align-items:center; justify-content:center; gap:8px;">
                                <i class="fas fa-info-circle"></i> اطلاعات NLP
                            </button>
                            <div id="testResult" style="margin-top:15px; padding:10px; border-radius:8px; display:none;"></div>
                        </div>
                    </div>
                    
                    <div class="sidebar-section">
                        <h3><i class="fas fa-lightbulb"></i> نکات کاربردی</h3>
                        <div>
                            <p><strong>✨ می‌توانید:</strong></p>
                            <ul style="padding-right: 20px; margin-top: 10px;">
                                <li style="margin-bottom: 8px; display: flex; align-items: flex-start; gap: 8px;">
                                    <i class="fas fa-check" style="color: #10b981; font-size: 0.9em;"></i>
                                    <span>در مورد هر موضوعی سوال بپرسید</span>
                                </li>
                                <li style="margin-bottom: 8px; display: flex; align-items: flex-start; gap: 8px;">
                                    <i class="fas fa-check" style="color: #10b981; font-size: 0.9em;"></i>
                                    <span>از دکمه‌های سریع استفاده کنید</span>
                                </li>
                                <li style="margin-bottom: 8px; display: flex; align-items: flex-start; gap: 8px;">
                                    <i class="fas fa-check" style="color: #10b981; font-size: 0.9em;"></i>
                                    <span>در مورد آخرین پست NLP بپرسید</span>
                                </li>
                                <li style="margin-bottom: 8px; display: flex; align-items: flex-start; gap: 8px;">
                                    <i class="fas fa-check" style="color: #10b981; font-size: 0.9em;"></i>
                                    <span>آمار تعاملات را مشاهده کنید</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            // نمایش اطلاعات NLP
            function showNlpInfo() {
                const message = "🔹 **آخرین پست صفحه NLP**: شماره 206\n📅 تاریخ: به‌زودی منتشر می‌شود\n📝 موضوع: پردازش زبان طبیعی پیشرفته\n✅ وضعیت: آماده انتشار\n\nاین پست جامع‌ترین مطلب در حوزه NLP فارسی خواهد بود!";
                window.natiqApp.addMessage(message, 'bot');
            }
            
            // تست API
            async function testApi() {
                const resultDiv = document.getElementById('testResult');
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = '<div style="color:#f59e0b; padding:10px; background:#fffbeb; border-radius:6px; text-align:center;">⏳ در حال تست اتصال...</div>';
                
                try {
                    const response = await fetch(window.natiqApp.baseUrl + '/api/health');
                    const data = await response.json();
                    
                    resultDiv.innerHTML = `
                        <div style="background:#d1fae5; color:#065f46; padding:12px; border-radius:6px;">
                            <strong style="display:block; margin-bottom:5px;">✅ تست موفق</strong>
                            <div style="font-size:0.9em;">
                                وضعیت: ${data.status}<br>
                                نسخه: ${data.version}<br>
                                سرویس: ${data.service}<br>
                                زمان: ${new Date(data.timestamp).toLocaleTimeString('fa-IR')}
                            </div>
                        </div>
                    `;
                } catch (error) {
                    resultDiv.innerHTML = `
                        <div style="background:#fee2e2; color:#7f1d1d; padding:12px; border-radius:6px;">
                            <strong style="display:block; margin-bottom:5px;">❌ خطا در تست</strong>
                            <div style="font-size:0.9em;">${error.message}</div>
                        </div>
                    `;
                }
                
                setTimeout(() => {
                    resultDiv.style.display = 'none';
                }, 5000);
            }
            
            // پاک کردن چت
            function clearChat() {
                if (confirm('آیا مطمئن هستید که می‌خواهید همه گفتگو را پاک کنید؟')) {
                    const messagesDiv = document.getElementById('messages');
                    const welcomeDiv = messagesDiv.querySelector('.welcome');
                    
                    while (messagesDiv.firstChild) {
                        messagesDiv.removeChild(messagesDiv.firstChild);
                    }
                    
                    if (welcomeDiv) {
                        messagesDiv.appendChild(welcomeDiv);
                    }
                    
                    window.natiqApp.messageCount = 0;
                    window.natiqApp.updateStats();
                    window.natiqApp.updateStatus('✅ گفتگو پاک شد');
                    
                    // اضافه کردن پیام تأیید
                    setTimeout(() => {
                        window.natiqApp.addMessage('گفتگو با موفقیت پاک شد. می‌توانید دوباره شروع کنید!', 'info');
                    }, 300);
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html_content)

# API Endpoints
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "natiq-ultimate",
        "version": "3.0.0",
        "environment": "vercel",
        "timestamp": datetime.now().isoformat(),
        "message": "سرور هوش مصنوعی فارسی به درستی کار می‌کند",
        "features": ["NLP فارسی", "پاسخ‌های هوشمند", "یادگیری مداوم", "رابط کاربری پیشرفته"]
    }

@app.post("/api/chat/{session_id}")
async def chat_endpoint(session_id: str, request: dict):
    try:
        question = request.get("message", "")
        
        if not question or question.strip() == "":
            raise HTTPException(status_code=400, detail="پیام نمی‌تواند خالی باشد")
        
        natiq = NatiqAdvancedAI()
        analysis = natiq.analyze_question(question)
        answer = natiq.generate_answer(question, analysis)
        
        return {
            "session_id": session_id,
            "question": question,
            "answer": answer,
            "analysis": analysis,
            "stats": natiq.stats,
            "timestamp": datetime.now().isoformat(),
            "version": "3.0.0"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "message": "خطا در پردازش سوال توسط هوش مصنوعی",
                "timestamp": datetime.now().isoformat()
            }
        )

# هندلر برای favicon.ico
@app.get("/favicon.ico")
async def favicon():
    return JSONResponse({"status": "no favicon"})

# برای Vercel
app = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
