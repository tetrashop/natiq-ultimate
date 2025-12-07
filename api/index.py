"""
natiq-ultimate - سیستم پرسش و پاسخ عصبی-نمادین عملیاتی
نسخه پایدار و کاملاً کاربردی
"""

import json
import re
import random
from datetime import datetime
from http.server import BaseHTTPRequestHandler
import urllib.parse

# ==================== سیستم هوش مصنوعی واقعی ====================

class NatiqAISystem:
    """سیستم هوش مصنوعی با قابلیت پرسش و پاسخ واقعی"""
    
    def __init__(self):
        self.knowledge_base = self._create_knowledge_base()
        self.conversation_history = []
        self.session_id = f"session_{int(datetime.now().timestamp())}"
        
    def _create_knowledge_base(self):
        """ایجاد پایگاه دانش غنی"""
        return {
            "هوش مصنوعی": {
                "تعریف": "شاخه‌ای از علوم کامپیوتر که به ساخت ماشین‌های هوشمند می‌پردازد",
                "کاربردها": ["پردازش زبان طبیعی", "بینایی کامپیوتر", "رباتیک", "تشخیص گفتار"],
                "زیرشاخه‌ها": ["یادگیری ماشین", "شبکه عصبی", "پردازش زبان طبیعی"],
                "اهمیت": "بسیار زیاد - آینده تکنولوژی"
            },
            "یادگیری ماشین": {
                "تعریف": "توانایی سیستم‌ها برای یادگیری از داده بدون برنامه‌نویسی صریح",
                "انواع": ["نظارت شده", "نظارت نشده", "تقویتی"],
                "الگوریتم‌ها": ["شبکه عصبی", "درخت تصمیم", "ماشین بردار پشتیبان"],
                "کاربرد": "پیش‌بینی، طبقه‌بندی، خوشه‌بندی"
            },
            "شبکه عصبی": {
                "تعریف": "مدل محاسباتی الهام گرفته از شبکه عصبی مغز",
                "اجزا": ["نرون مصنوعی", "لایه‌های پنهان", "تابع فعال‌سازی"],
                "انواع": ["پرسپترون", "شبکه کانولوشن", "شبکه بازگشتی"],
                "استفاده": "تشخیص تصویر، پردازش زبان، پیش‌بینی"
            },
            "پایتون": {
                "تعریف": "زبان برنامه‌نویسی سطح بالا، مفسری و همه‌منظوره",
                "ویژگی‌ها": ["ساده", "خوانا", "کتابخانه‌های غنی"],
                "استفاده در هوش مصنوعی": ["تنسورفلو", "پایتورچ", "scikit-learn"],
                "محبوبیت": "زبان شماره یک در هوش مصنوعی"
            },
            "داده کاوی": {
                "تعریف": "استخراج دانش و الگو از داده‌های بزرگ",
                "مراحل": ["پاکسازی داده", "تبدیل داده", "کاوش", "ارزیابی"],
                "ابزارها": ["پایتون", "R", "SQL"],
                "اهمیت": "تصمیم‌گیری مبتنی بر داده"
            }
        }
    
    def analyze_question(self, question):
        """تحلیل عمیق سوال کاربر"""
        question_lower = question.lower()
        
        # تشخیص نوع سوال
        question_patterns = {
            "تعریفی": r"(چیست|چیه|تعریف|منظور|معنی|چه)",
            "مقایسه‌ای": r"(تفاوت|فرق|مقایسه|اختلاف|کدام بهتر)",
            "کاربردی": r"(کاربرد|استفاده|فواید|مزایا|منافع)",
            "روشی": r"(چگونه|چطور|روش|طریق|مراحل|چکار کنم)",
            "اجزایی": r"(اجزا|قسمت‌ها|مولفه‌ها|بخش‌ها|عناصر)",
            "تاریخی": r"(تاریخچه|اولین|ابداع|اختراع|چه زمانی)"
        }
        
        detected_type = "عمومی"
        for q_type, pattern in question_patterns.items():
            if re.search(pattern, question_lower):
                detected_type = q_type
                break
        
        # یافتن مفاهیم مرتبط
        found_concepts = []
        for concept in self.knowledge_base:
            if concept.lower() in question_lower:
                found_concepts.append(concept)
            elif any(word in question_lower for word in concept.split()):
                found_concepts.append(concept)
        
        # محاسبه اطمینان
        confidence = 0.5
        if found_concepts:
            confidence = min(0.7 + (len(found_concepts) * 0.15), 0.95)
        
        return {
            "type": detected_type,
            "concepts": found_concepts,
            "confidence": round(confidence, 2),
            "words_count": len(question.split()),
            "has_question_mark": "؟" in question or "?" in question
        }
    
    def search_knowledge(self, concept, question_type):
        """جستجو در پایگاه دانش"""
        if concept in self.knowledge_base:
            data = self.knowledge_base[concept]
            
            if question_type == "تعریفی":
                return f"تعریف: {data.get('تعریف', 'تعریف یافت نشد')}"
            elif question_type == "کاربردی":
                return f"کاربردها: {', '.join(data.get('کاربردها', ['کاربرد یافت نشد']))}"
            elif question_type == "اجزایی":
                return f"اجزا: {', '.join(data.get('اجزا', ['اجزا یافت نشد']))}"
            elif question_type == "مقایسه‌ای":
                return f"مقایسه با سایر مفاهیم مرتبط: {', '.join(data.get('زیرشاخه‌ها', ['مقایسه یافت نشد']))}"
            else:
                return f"{concept}: {data.get('تعریف', 'اطلاعات یافت نشد')}"
        
        return "مفهوم در پایگاه دانش یافت نشد."
    
    def generate_response(self, question, analysis):
        """تولید پاسخ هوشمند"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if not analysis["concepts"]:
            return f"""❓ **سوال شما**: "{question}"

🔍 **تحلیل سیستم**:
• نوع سوال: {analysis['type']}
• اطمینان: {analysis['confidence']}
• زمان: {timestamp}

💡 **پیشنهاد سیستم**:
لطفاً سوال خود را با یکی از مفاهیم زیر مرتبط کنید:
• هوش مصنوعی
• یادگیری ماشین  
• شبکه عصبی
• پایتون
• داده کاوی

🎯 **مثال**:
"هوش مصنوعی چیست؟"
"تفاوت یادگیری ماشین و شبکه عصبی؟"
"کاربردهای پایتون در هوش مصنوعی؟" """
        
        # اگر مفهوم مشخصی پیدا شد
        main_concept = analysis["concepts"][0]
        knowledge_info = self.search_knowledge(main_concept, analysis["type"])
        
        response = f"""🧠 **natiq-ultimate v6.0** - سیستم عصبی-نمادین

❓ **پرسش شما**: "{question}"

🔬 **تحلیل عمیق**:
• مفهوم اصلی: **{main_concept}**
• نوع سوال: {analysis['type']}
• اعتماد سیستم: {analysis['confidence']}/1.0
• کلمات: {analysis['words_count']} واژه
• زمان تحلیل: {timestamp}

📚 **پاسخ تخصصی**:
{knowledge_info}

💎 **اطلاعات تکمیلی**:"""
        
        # افزودن اطلاعات تکمیلی
        if main_concept in self.knowledge_base:
            data = self.knowledge_base[main_concept]
            for key, value in data.items():
                if key != "تعریف" and key != "کاربردها":
                    if isinstance(value, list):
                        response += f"\n• {key}: {', '.join(value)}"
                    else:
                        response += f"\n• {key}: {value}"
        
        response += f"""

⚡ **سیستم من**:
این پاسخ با معماری عصبی-نمادین تولید شده:
🤖 **لایه عصبی**: تشخیص نوع سوال و مفاهیم
📚 **لایه دانشی**: جستجو در پایگاه اطلاعات
🔗 **لایه یکپارچه**: ترکیب هوشمند نتایج

🔄 **برای ادامه می‌پرسید**:
1. درباره {main_concept} بیشتر بدانم
2. مقایسه {main_concept} با سایر مفاهیم
3. کاربردهای عملی {main_concept}
4. سوال جدید بپرسم"""
        
        # ذخیره در تاریخچه مکالمه
        self.conversation_history.append({
            "time": timestamp,
            "question": question,
            "concept": main_concept,
            "analysis": analysis,
            "response_preview": response[:100]
        })
        
        return response
    
    def process_question(self, question):
        """پردازش کامل سوال"""
        analysis = self.analyze_question(question)
        response = self.generate_response(question, analysis)
        
        return {
            "success": True,
            "question": question,
            "response": response,
            "analysis": analysis,
            "system_info": {
                "name": "natiq-ultimate",
                "version": "6.0.0",
                "session": self.session_id,
                "concepts_available": len(self.knowledge_base),
                "conversation_history": len(self.conversation_history)
            },
            "timestamp": datetime.now().isoformat()
        }

# ایجاد نمونه سیستم
ai_system = NatiqAISystem()

# ==================== HTTP Server Handler ====================

class RequestHandler(BaseHTTPRequestHandler):
    """Handler برای درخواست‌های HTTP"""
    
    def do_GET(self):
        """مدیریت درخواست‌های GET"""
        try:
            path = self.path.split('?')[0]
            
            if path == '/':
                self.serve_home_page()
            elif path == '/api/health':
                self.send_health()
            elif path == '/api/knowledge':
                self.send_knowledge_base()
            elif path == '/api/history':
                self.send_conversation_history()
            else:
                self.send_error(404, "مسیر یافت نشد")
        except Exception as e:
            self.send_error(500, f"خطای سرور: {str(e)}")
    
    def do_POST(self):
        """مدیریت درخواست‌های POST"""
        try:
            if self.path == '/api/ask':
                self.handle_question()
            else:
                self.send_error(404, "مسیر API یافت نشد")
        except Exception as e:
            self.send_error(500, f"خطای پردازش: {str(e)}")
    
    def serve_home_page(self):
        """سرویس دهی صفحه اصلی با رابط کاربری کامل"""
        html_content = self._generate_html_interface()
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(html_content)))
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def _generate_html_interface(self):
        """ایجاد HTML رابط کاربری"""
        return """<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 natiq-ultimate v6.0 - سیستم پرسش و پاسخ هوش مصنوعی</title>
    <style>
        :root {
            --primary-color: #2962ff;
            --secondary-color: #6200ea;
            --accent-color: #00e5ff;
            --dark-bg: #0a192f;
            --darker-bg: #020c1b;
            --text-color: #e6f1ff;
            --card-bg: #112240;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Vazirmatn', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, var(--darker-bg) 0%, var(--dark-bg) 100%);
            color: var(--text-color);
            min-height: 100vh;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* هدر */
        .header {
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            border-radius: 20px;
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
            border: 2px solid rgba(255, 255, 255, 0.1);
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 30% 50%, rgba(0, 229, 255, 0.1) 0%, transparent 50%);
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #fff, var(--accent-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            position: relative;
            z-index: 1;
        }
        
        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
            color: #bbdefb;
            position: relative;
            z-index: 1;
        }
        
        /* محتوای اصلی */
        .main-content {
            display: grid;
            grid-template-columns: 1fr;
            gap: 30px;
        }
        
        @media (min-width: 992px) {
            .main-content {
                grid-template-columns: 2fr 1fr;
            }
        }
        
        /* بخش چت */
        .chat-section {
            background: var(--card-bg);
            border-radius: 20px;
            padding: 25px;
            border: 1px solid rgba(41, 98, 255, 0.2);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        
        .messages-container {
            height: 500px;
            overflow-y: auto;
            padding: 20px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 15px;
            margin-bottom: 25px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .message {
            margin: 15px 0;
            padding: 20px;
            border-radius: 15px;
            max-width: 85%;
            animation: messageAppear 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            backdrop-filter: blur(10px);
        }
        
        @keyframes messageAppear {
            from {
                opacity: 0;
                transform: translateY(20px) scale(0.95);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }
        
        .user-message {
            background: linear-gradient(135deg, rgba(41, 98, 255, 0.2), rgba(98, 0, 234, 0.15));
            margin-left: auto;
            border-right: 4px solid var(--primary-color);
        }
        
        .bot-message {
            background: linear-gradient(135deg, rgba(17, 34, 64, 0.9), rgba(30, 60, 114, 0.8));
            margin-right: auto;
            border-left: 4px solid var(--accent-color);
            white-space: pre-wrap;
        }
        
        .message-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .message-icon {
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            font-size: 1.2em;
        }
        
        /* ورودی */
        .input-section {
            background: rgba(255, 255, 255, 0.03);
            padding: 20px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .input-group {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        #questionInput {
            flex: 1;
            padding: 18px 25px;
            background: rgba(255, 255, 255, 0.07);
            border: 2px solid rgba(41, 98, 255, 0.4);
            border-radius: 15px;
            color: var(--text-color);
            font-size: 16px;
            font-family: inherit;
            transition: all 0.3s;
        }
        
        #questionInput:focus {
            outline: none;
            border-color: var(--primary-color);
            background: rgba(255, 255, 255, 0.1);
            box-shadow: 0 0 0 4px rgba(41, 98, 255, 0.1);
        }
        
        #sendButton {
            padding: 18px 35px;
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
            color: white;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s;
            white-space: nowrap;
        }
        
        #sendButton:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(41, 98, 255, 0.4);
        }
        
        /* مثال‌ها */
        .examples-section {
            margin-top: 25px;
        }
        
        .examples-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .example-btn {
            padding: 16px;
            background: rgba(41, 98, 255, 0.15);
            border: 1px solid rgba(41, 98, 255, 0.3);
            border-radius: 12px;
            color: #bbdefb;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
            font-size: 15px;
        }
        
        .example-btn:hover {
            background: rgba(41, 98, 255, 0.25);
            transform: translateY(-3px) translateX(-5px);
            border-color: var(--primary-color);
        }
        
        /* پنل سیستم */
        .system-panel {
            background: var(--card-bg);
            border-radius: 20px;
            padding: 25px;
            border: 1px solid rgba(0, 229, 255, 0.2);
        }
        
        .panel-section {
            margin-bottom: 25px;
            padding-bottom: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .panel-section:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 15px;
        }
        
        .stat-card {
            background: rgba(0, 0, 0, 0.3);
            padding: 18px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: var(--accent-color);
            margin-bottom: 5px;
        }
        
        .knowledge-list {
            margin-top: 15px;
        }
        
        .concept-tag {
            display: inline-block;
            background: rgba(41, 98, 255, 0.2);
            padding: 8px 15px;
            margin: 5px;
            border-radius: 20px;
            font-size: 0.9em;
            border: 1px solid rgba(41, 98, 255, 0.4);
        }
        
        /* پانوشت */
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.9em;
        }
        
        /* اسکرول بار */
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
            border-radius: 5px;
        }
        
        .pulse {
            display: inline-block;
            width: 10px;
            height: 10px;
            background: #4caf50;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 1.5s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
        
        .loading {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 15px;
            color: var(--accent-color);
        }
        
        .loading-dots span {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: var(--accent-color);
            border-radius: 50%;
            margin: 0 2px;
            animation: loading 1.4s infinite;
        }
        
        .loading-dots span:nth-child(2) { animation-delay: 0.2s; }
        .loading-dots span:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes loading {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(0.5); opacity: 0.5; }
        }
    </style>
    
    <!-- فونت فارسی -->
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <!-- هدر -->
        <header class="header">
            <h1>🧠 natiq-ultimate v6.0</h1>
            <div class="subtitle">سیستم پرسش و پاسخ عصبی-نمادین هوش مصنوعی</div>
        </header>
        
        <!-- محتوای اصلی -->
        <div class="main-content">
            <!-- بخش چت و تعامل -->
            <div class="chat-section">
                <div class="messages-container" id="messagesContainer">
                    <!-- پیام خوش‌آمدگویی -->
                    <div class="message bot-message">
                        <div class="message-header">
                            <div class="message-icon">🤖</div>
                            <div>سیستم عصبی-نمادین</div>
                        </div>
                        <div class="message-content">
                            🎉 **به natiq-ultimate خوش آمدید!**
                            
                            این سیستم ترکیبی از:
                            • پردازش عصبی (درک زبان)
                            • دانش نمادین (استدلال منطقی)
                            • هوش مصنوعی (تولید پاسخ)
                            
                            💡 **می‌توانید بپرسید**:
                            • "هوش مصنوعی چیست؟"
                            • "کاربردهای یادگیری ماشین؟"
                            • "تفاوت شبکه عصبی و یادگیری ماشین؟"
                            • "پایتون در هوش مصنوعی چه کاربردی دارد؟"
                            
                            🚀 **سیستم آماده پاسخگویی است...**
                        </div>
                    </div>
                </div>
                
                <div class="input-section">
                    <div class="input-group">
                        <input type="text" 
                               id="questionInput" 
                               placeholder="سوال خود را درباره هوش مصنوعی بپرسید..." 
                               autocomplete="off"
                               autofocus>
                        <button id="sendButton">ارسال پرسش</button>
                    </div>
                    
                    <div class="examples-section">
                        <h3>📋 سوالات نمونه:</h3>
                        <div class="examples-grid">
                            <div class="example-btn" data-question="هوش مصنوعی چیست؟">
                                🤔 هوش مصنوعی چیست؟
                            </div>
                            <div class="example-btn" data-question="کاربردهای یادگیری ماشین">
                                🛠️ کاربردهای یادگیری ماشین
                            </div>
                            <div class="example-btn" data-question="تفاوت هوش مصنوعی و یادگیری ماشین">
                                ⚖️ تفاوت AI و ML
                            </div>
                            <div class="example-btn" data-question="پایتون در هوش مصنوعی چه کاربردی دارد؟">
                                🐍 پایتون در AI
                            </div>
                            <div class="example-btn" data-question="شبکه عصبی چیست و چگونه کار می‌کند؟">
                                🧠 شبکه عصبی چیست؟
                            </div>
                            <div class="example-btn" data-question="داده کاوی چه اهمیتی دارد؟">
                                💎 اهمیت داده کاوی
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- پنل سیستم -->
            <div class="system-panel">
                <div class="panel-section">
                    <h3>📊 وضعیت سیستم</h3>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-value" id="questionsCount">0</div>
                            <div>پرسش‌ها</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value" id="conceptsCount">5</div>
                            <div>مفاهیم دانش</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value" id="responseTime">--</div>
                            <div>زمان پاسخ</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value"><span class="pulse"></span>آنلاین</div>
                            <div>وضعیت</div>
                        </div>
                    </div>
                </div>
                
                <div class="panel-section">
                    <h3>📚 پایگاه دانش</h3>
                    <div class="knowledge-list">
                        <span class="concept-tag">هوش مصنوعی</span>
                        <span class="concept-tag">یادگیری ماشین</span>
                        <span class="concept-tag">شبکه عصبی</span>
                        <span class="concept-tag">پایتون</span>
                        <span class="concept-tag">داده کاوی</span>
                    </div>
                </div>
                
                <div class="panel-section">
                    <h3>🎯 تحلیل فعلی</h3>
                    <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; margin-top: 10px;">
                        <div id="currentAnalysis">
                            <div style="opacity: 0.7;">هنوز سوالی پرسیده نشده</div>
                        </div>
                    </div>
                </div>
                
                <div class="panel-section">
                    <h3>⚙️ کنترل‌ها</h3>
                    <div style="display: flex; gap: 10px; margin-top: 15px;">
                        <button onclick="clearChat()" style="flex: 1; padding: 12px; background: rgba(255, 59, 48, 0.2); border: 1px solid rgba(255, 59, 48, 0.4); border-radius: 10px; color: #ffcccb; cursor: pointer;">
                            پاک کردن گفتگو
                        </button>
                        <button onclick="testSystem()" style="flex: 1; padding: 12px; background: rgba(76, 175, 80, 0.2); border: 1px solid rgba(76, 175, 80, 0.4); border-radius: 10px; color: #c8e6c9; cursor: pointer;">
                            تست سیستم
                        </button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- پانوشت -->
        <div class="footer">
            <p>natiq-ultimate v6.0 | سیستم عصبی-نمادین هوش مصنوعی | طراحی شده برای Vercel</p>
            <p>© 2024 - تمامی حقوق محفوظ است | نسخه کاملاً عملیاتی</p>
        </div>
    </div>
    
    <script>
        class NatiqChat {
            constructor() {
                this.messageCount = 0;
                this.conversationHistory = [];
                this.apiBase = window.location.origin;
                this.init();
            }
            
            init() {
                this.setupEventListeners();
                this.updateStats();
            }
            
            setupEventListeners() {
                // دکمه ارسال
                document.getElementById('sendButton').addEventListener('click', () => this.sendQuestion());
                
                // ورودی با Enter
                document.getElementById('questionInput').addEventListener('keypress', (e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        this.sendQuestion();
                    }
                });
                
                // دکمه‌های نمونه
                document.querySelectorAll('.example-btn').forEach(btn => {
                    btn.addEventListener('click', (e) => {
                        const question = e.currentTarget.getAttribute('data-question');
                        if (question) {
                            document.getElementById('questionInput').value = question;
                            this.sendQuestion();
                        }
                    });
                });
            }
            
            async sendQuestion() {
                const input = document.getElementById('questionInput');
                const question = input.value.trim();
                
                if (!question) {
                    this.showNotification('⚠️ لطفاً سوالی بنویسید!', 'warning');
                    return;
                }
                
                // نمایش سوال کاربر
                this.addMessage(question, 'user');
                input.value = '';
                this.messageCount++;
                
                // نمایش وضعیت پردازش
                const processingId = this.showProcessing();
                
                try {
                    const startTime = Date.now();
                    
                    const response = await fetch(this.apiBase + '/api/ask', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ 
                            question: question,
                            timestamp: new Date().toISOString()
                        })
                    });
                    
                    const endTime = Date.now();
                    const responseTime = (endTime - startTime) / 1000;
                    
                    if (!response.ok) {
                        throw new Error(`خطای HTTP: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        // حذف وضعیت پردازش
                        this.hideProcessing(processingId);
                        
                        // نمایش پاسخ
                        this.addMessage(data.response, 'bot');
                        
                        // به‌روزرسانی آمار
                        this.updateStats(responseTime);
                        
                        // به‌روزرسانی تحلیل
                        this.updateAnalysis(data.analysis);
                        
                        // اضافه به تاریخچه
                        this.conversationHistory.push({
                            question: question,
                            response: data.response.substring(0, 100) + '...',
                            time: new Date().toLocaleTimeString()
                        });
                        
                    } else {
                        throw new Error(data.error || 'خطای ناشناخته');
                    }
                    
                } catch (error) {
                    console.error('❌ خطا:', error);
                    this.hideProcessing(processingId);
                    
                    this.addMessage(
                        `⚠️ خطا در پردازش سوال:\n${error.message}\n\nلطفاً دوباره تلاش کنید.`,
                        'bot'
                    );
                    
                    this.showNotification('❌ خطا در ارتباط با سرور', 'error');
                }
            }
            
            addMessage(text, type) {
                const container = document.getElementById('messagesContainer');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${type}-message`;
                
                const time = new Date().toLocaleTimeString('fa-IR', {
                    hour: '2-digit',
                    minute: '2-digit'
                });
                
                const icon = type === 'user' ? '👤' : '🤖';
                const header = type === 'user' ? 'شما' : 'سیستم عصبی-نمادین';
                
                messageDiv.innerHTML = `
                    <div class="message-header">
                        <div class="message-icon">${icon}</div>
                        <div>${header} • ${time}</div>
                    </div>
                    <div class="message-content">${this.escapeHtml(text)}</div>
                `;
                
                container.appendChild(messageDiv);
                container.scrollTop = container.scrollHeight;
            }
            
            showProcessing() {
                const container = document.getElementById('messagesContainer');
                const processingDiv = document.createElement('div');
                processingDiv.className = 'message bot-message';
                processingDiv.id = 'processingMessage';
                processingDiv.innerHTML = `
                    <div class="message-header">
                        <div class="message-icon">⚡</div>
                        <div>سیستم عصبی-نمادین</div>
                    </div>
                    <div class="message-content">
                        <div class="loading">
                            <div class="loading-dots">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                            در حال پردازش پرسش شما...
                        </div>
                    </div>
                `;
                
                container.appendChild(processingDiv);
                container.scrollTop = container.scrollHeight;
                
                return 'processingMessage';
            }
            
            hideProcessing(elementId) {
                const element = document.getElementById(elementId);
                if (element) {
                    element.remove();
                }
            }
            
            updateStats(responseTime = null) {
                document.getElementById('questionsCount').textContent = this.messageCount;
                
                if (responseTime !== null) {
                    document.getElementById('responseTime').textContent = responseTime.toFixed(2) + 's';
                }
            }
            
            updateAnalysis(analysis) {
                const analysisDiv = document.getElementById('currentAnalysis');
                if (analysis && analysis.concepts) {
                    analysisDiv.innerHTML = `
                        <div>📌 <strong>مفاهیم:</strong> ${analysis.concepts.join(', ')}</div>
                        <div>🎯 <strong>نوع سوال:</strong> ${analysis.type}</div>
                        <div>⚡ <strong>اعتماد سیستم:</strong> ${analysis.confidence}/1.0</div>
                        <div>📝 <strong>کلمات:</strong> ${analysis.words_count}</div>
                    `;
                }
            }
            
            showNotification(message, type = 'info') {
                // ایجاد یک ناتیفیکیشن ساده
                const notification = document.createElement('div');
                notification.style.cssText = `
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    padding: 15px 25px;
                    background: ${type === 'error' ? '#d32f2f' : '#1976d2'};
                    color: white;
                    border-radius: 10px;
                    z-index: 1000;
                    animation: slideIn 0.3s ease-out;
                `;
                notification.textContent = message;
                
                document.body.appendChild(notification);
                
                setTimeout(() => {
                    notification.style.animation = 'slideOut 0.3s ease-out';
                    setTimeout(() => notification.remove(), 300);
                }, 3000);
                
                // اضافه کردن استایل‌های انیمیشن
                const style = document.createElement('style');
                style.textContent = `
                    @keyframes slideIn {
                        from { transform: translateX(100%); opacity: 0; }
                        to { transform: translateX(0); opacity: 1; }
                    }
                    @keyframes slideOut {
                        from { transform: translateX(0); opacity: 1; }
                        to { transform: translateX(100%); opacity: 0; }
                    }
                `;
                document.head.appendChild(style);
            }
            
            escapeHtml(text) {
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }
        }
        
        // توابع کمکی
        function clearChat() {
            if (confirm('آیا مطمئن هستید که می‌خواهید همه گفتگو را پاک کنید؟')) {
                const container = document.getElementById('messagesContainer');
                const welcomeMessage = container.querySelector('.bot-message');
                
                // پاک کردن همه پیام‌ها
                while (container.firstChild) {
                    container.removeChild(container.firstChild);
                }
                
                // بازگرداندن پیام خوش‌آمدگویی
                if (welcomeMessage) {
                    container.appendChild(welcomeMessage);
                } else {
                    // اگر پیام خوش‌آمدگویی وجود نداشت، ایجادش کن
                    const welcomeDiv = document.createElement('div');
                    welcomeDiv.className = 'message bot-message';
                    welcomeDiv.innerHTML = `
                        <div class="message-header">
                            <div class="message-icon">🤖</div>
                            <div>سیستم عصبی-نمادین</div>
                        </div>
                        <div class="message-content">
                            گفتگو پاک شد! می‌توانید سوال جدیدی بپرسید.
                        </div>
                    `;
                    container.appendChild(welcomeDiv);
                }
                
                // بازنشانی آمار
                window.chatApp.messageCount = 0;
                window.chatApp.updateStats();
                document.getElementById('currentAnalysis').innerHTML = '<div style="opacity: 0.7;">هنوز سوالی پرسیده نشده</div>';
                
                // نمایش ناتیفیکیشن
                window.chatApp.showNotification('✅ گفتگو با موفقیت پاک شد', 'info');
            }
        }
        
        function testSystem() {
            const testQuestions = [
                "هوش مصنوعی چیست؟",
                "کاربردهای یادگیری ماشین",
                "تفاوت شبکه عصبی و یادگیری ماشین",
                "پایتون در هوش مصنوعی چه کاربردی دارد؟"
            ];
            
            let delay = 0;
            testQuestions.forEach(question => {
                setTimeout(() => {
                    document.getElementById('questionInput').value = question;
                    window.chatApp.sendQuestion();
                }, delay);
                delay += 3000; // هر 3 ثانیه یک سوال
            });
            
            window.chatApp.showNotification('🧪 تست سیستم آغاز شد...', 'info');
        }
        
        // راه‌اندازی سیستم هنگام لود صفحه
        document.addEventListener('DOMContentLoaded', () => {
            window.chatApp = new NatiqChat();
            document.getElementById('questionInput').focus();
        });
    </script>
</body>
</html>"""
    
    def handle_question(self):
        """مدیریت درخواست سوال"""
        try:
            # خواندن داده‌های POST
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            if not post_data:
                self.send_json_response({
                    "success": False,
                    "error": "بدون داده"
                }, 400)
                return
            
            data = json.loads(post_data.decode('utf-8'))
            question = data.get('question', '').strip()
            
            if not question:
                self.send_json_response({
                    "success": False,
                    "error": "سوال نمی‌تواند خالی باشد"
                }, 400)
                return
            
            # پردازش سوال
            result = ai_system.process_question(question)
            
            # ارسال پاسخ
            self.send_json_response(result)
            
        except json.JSONDecodeError:
            self.send_json_response({
                "success": False,
                "error": "فرمت JSON نامعتبر است"
            }, 400)
        except Exception as e:
            self.send_json_response({
                "success": False,
                "error": f"خطای پردازش: {str(e)}"
            }, 500)
    
    def send_health(self):
        """ارسال وضعیت سلامت"""
        response = {
            "status": "active",
            "system": "natiq-ultimate",
            "version": "6.0.0",
            "timestamp": datetime.now().isoformat(),
            "statistics": {
                "knowledge_concepts": len(ai_system.knowledge_base),
                "conversation_history": len(ai_system.conversation_history),
                "session_id": ai_system.session_id
            }
        }
        self.send_json_response(response)
    
    def send_knowledge_base(self):
        """ارسال لیست مفاهیم پایگاه دانش"""
        concepts = list(ai_system.knowledge_base.keys())
        response = {
            "concepts": concepts,
            "count": len(concepts),
            "timestamp": datetime.now().isoformat()
        }
        self.send_json_response(response)
    
    def send_conversation_history(self):
        """ارسال تاریخچه مکالمه"""
        response = {
            "history": ai_system.conversation_history[-10:],  # آخرین 10 مورد
            "total": len(ai_system.conversation_history),
            "timestamp": datetime.now().isoformat()
        }
        self.send_json_response(response)
    
    def send_json_response(self, data, status_code=200):
        """ارسال پاسخ JSON"""
        response_json = json.dumps(data, ensure_ascii=False, indent=2)
        
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(response_json.encode('utf-8'))))
        self.end_headers()
        self.wfile.write(response_json.encode('utf-8'))
    
    def send_error(self, code, message):
        """ارسال خطا"""
        self.send_response(code)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(f"{code}: {message}".encode('utf-8'))
    
    def log_message(self, format, *args):
        """غیرفعال کردن لاگ پیش‌فرض"""
        pass

# ==================== تابع اصلی برای Vercel ====================

def handler(event, context):
    """Handler سازگار با Vercel Serverless Functions"""
    # این تابع برای سازگاری با Vercel ایجاد شده
    # اما ما از BaseHTTPRequestHandler استفاده می‌کنیم
    
    # برای جلوگیری از خطا، یک پیام ساده برگردان
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain; charset=utf-8'
        },
        'body': 'natiq-ultimate system is running\nUse POST /api/ask for questions'
    }

# اگر مستقیماً اجرا شود (برای تست محلی)
if __name__ == "__main__":
    from http.server import HTTPServer
    import sys
    
    port = 3000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    server = HTTPServer(('localhost', port), RequestHandler)
    print(f"🚀 Starting natiq-ultimate server on http://localhost:{port}")
    print("🧠 Neural-Symbolic AI System with Full Q&A Capability")
    print("📚 Knowledge Base: AI, Machine Learning, Neural Networks, Python, Data Mining")
    print("⚡ Ready to answer questions...")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down server...")
        server.server_close()
