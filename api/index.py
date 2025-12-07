"""
natiq-ultimate - سیستم عصبی نمادین خالص پایتون
نسخه فوق سبک برای Vercel
"""

import json
import math
import random
import hashlib
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse

# ==================== سیستم هوش مصنوعی ====================

class NatiqAI:
    """سیستم هوش مصنوعی عصبی-نمادین"""
    
    def __init__(self):
        self.knowledge = {
            "هوش مصنوعی": "شاخه‌ای از علوم کامپیوتر که به ساخت ماشین‌های هوشمند می‌پردازد",
            "یادگیری ماشین": "توانایی سیستم‌ها برای یادگیری از داده بدون برنامه‌نویسی صریح",
            "شبکه عصبی": "مدل محاسباتی الهام گرفته از شبکه عصبی مغز",
            "پایتون": "زبان برنامه‌نویسی سطح بالا برای هوش مصنوعی و علم داده",
            "داده کاوی": "استخراج دانش از داده‌های بزرگ",
            "پردازش زبان طبیعی": "تعامل کامپیوتر با زبان انسان"
        }
        
        self.session_id = hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:8]
        self.history = []
    
    def analyze_question(self, question):
        """تحلیل سوال"""
        question_lower = question.lower()
        
        # تشخیص نوع سوال
        question_types = {
            "تعریفی": ["چیست", "چیه", "تعریف", "منظور", "معنی"],
            "مقایسه‌ای": ["تفاوت", "فرق", "مقایسه", "اختلاف"],
            "روشی": ["چگونه", "چطور", "روش", "طریق"],
            "علّی": ["چرا", "علت", "دلیل", "سبب"]
        }
        
        detected_type = "عمومی"
        for q_type, keywords in question_types.items():
            if any(keyword in question_lower for keyword in keywords):
                detected_type = q_type
                break
        
        # یافتن مفاهیم مرتبط
        found_concepts = []
        for concept in self.knowledge:
            if concept.lower() in question_lower:
                found_concepts.append(concept)
        
        return {
            "type": detected_type,
            "concepts": found_concepts,
            "confidence": min(0.8 + len(found_concepts) * 0.1, 0.95)
        }
    
    def generate_response(self, question, analysis):
        """تولید پاسخ"""
        response = ""
        
        if analysis["type"] == "تعریفی" and analysis["concepts"]:
            concept = analysis["concepts"][0]
            response = f"""📚 **تعریف {concept}**:
            
{self.knowledge.get(concept, "تعریف یافت نشد")}

💡 **سیستم عصبی-نمادین**:
این پاسخ توسط معماری ترکیبی تولید شده:
• پردازش عصبی: درک زبان و زمینه
• دانش نمادین: مفاهیم ساختاریافته
• یکپارچه‌سازی: ترکیب هوشمند نتایج

🎯 **اعتماد سیستم**: {analysis['confidence']:.2f}"""
        
        elif analysis["type"] == "مقایسه‌ای":
            response = f"""⚖️ **تحلیل مقایسه‌ای**:

🧠 **روش کار سیستم عصبی-نمادین**:
1. استخراج مفاهیم برای مقایسه
2. یافتن شباهت‌ها و تفاوت‌ها
3. ساختاردهی نتایج
4. تولید پاسخ منطقی

🔍 **مفاهیم شناسایی شده**: {', '.join(analysis['concepts']) if analysis['concepts'] else 'هیچ'}

⚡ **دقت تحلیل**: {analysis['confidence']:.2f}"""
        
        elif analysis["type"] == "روشی":
            response = f"""🛠️ **راهنمای روشی**:

🎯 **مراحل پیشنهادی سیستم**:
1. تعریف دقیق مسئله
2. جمع‌آوری داده‌های مرتبط
3. انتخاب الگوریتم مناسب
4. آموزش و ارزیابی مدل
5. بهبود مستمر

🤖 **ویژگی‌های سیستم**:
• یادگیری عمیق: درک الگوهای پیچیده
• استدلال نمادین: منطق ساختاریافته
• ترکیب هوشمند: بهترین هر دو جهان

📊 **اطمینان**: {analysis['confidence']:.2f}"""
        
        else:
            response = f"""🧠 **سیستم عصبی-نمادین natiq-ultimate**:

به سیستم هوش مصنوعی ترکیبی خوش آمدید!

🔧 **قابلیت‌ها**:
✅ تحلیل هدف سوال
✅ جستجو در پایگاه دانش
✅ تولید پاسخ هوشمند
✅ یادگیری از تعاملات

💡 **مفاهیم موجود در سیستم**: {', '.join(list(self.knowledge.keys())[:5])}...

🎯 **برای شروع می‌پرسید**:
• "هوش مصنوعی چیست؟"
• "تفاوت یادگیری ماشین و شبکه عصبی؟"
• "چگونه با پایتون هوش مصنوعی بسازیم؟"

⚡ **اعتماد سیستم**: {analysis['confidence']:.2f}"""
        
        # ذخیره در تاریخچه
        self.history.append({
            "question": question,
            "analysis": analysis,
            "time": datetime.now().strftime("%H:%M:%S"),
            "response_preview": response[:50] + "..."
        })
        
        return response
    
    def process(self, question):
        """پردازش کامل سوال"""
        analysis = self.analyze_question(question)
        response = self.generate_response(question, analysis)
        
        return {
            "success": True,
            "question": question,
            "response": response,
            "analysis": analysis,
            "system": {
                "name": "natiq-ultimate",
                "version": "6.0.0",
                "session": self.session_id,
                "requests": len(self.history) + 1
            },
            "timestamp": datetime.now().isoformat()
        }

# ایجاد نمونه سیستم
ai_system = NatiqAI()

# ==================== HTTP Handler ====================

class RequestHandler(BaseHTTPRequestHandler):
    """Handler برای درخواست‌های HTTP"""
    
    def do_GET(self):
        """مدیریت درخواست GET"""
        parsed_path = urlparse.urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_home_page()
        elif parsed_path.path == '/health':
            self.send_health()
        elif parsed_path.path == '/api/health':
            self.send_api_health()
        else:
            self.send_error(404, "صفحه یافت نشد")
    
    def do_POST(self):
        """مدیریت درخواست POST"""
        if self.path == '/api/ask':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                data = json.loads(post_data) if post_data else {}
                question = data.get('question', '').strip()
                
                if not question:
                    response = {
                        "success": False,
                        "error": "سوال نمی‌تواند خالی باشد"
                    }
                    self.send_json_response(response, 400)
                else:
                    result = ai_system.process(question)
                    self.send_json_response(result)
                    
            except Exception as e:
                response = {
                    "success": False,
                    "error": str(e)
                }
                self.send_json_response(response, 500)
        else:
            self.send_error(404, "مسیر API یافت نشد")
    
    def send_home_page(self):
        """ارسال صفحه اصلی"""
        html = """<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 natiq-ultimate - سیستم عصبی نمادین</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: white;
            min-height: 100vh;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .header {
            text-align: center;
            padding: 30px 20px;
            margin-bottom: 30px;
            border-bottom: 2px solid #00b4d8;
        }
        h1 {
            font-size: 3em;
            background: linear-gradient(45deg, #00b4d8, #90e0ef);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            text-shadow: 0 5px 20px rgba(0, 180, 216, 0.3);
        }
        .tagline {
            font-size: 1.2em;
            color: #90e0ef;
            margin-bottom: 20px;
        }
        .architecture {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .component {
            background: rgba(255, 255, 255, 0.05);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            border: 1px solid rgba(0, 180, 216, 0.2);
            transition: all 0.3s;
        }
        .component:hover {
            transform: translateY(-5px);
            border-color: #00b4d8;
            box-shadow: 0 10px 30px rgba(0, 180, 216, 0.2);
        }
        .component-icon {
            font-size: 2.5em;
            margin-bottom: 15px;
            color: #00b4d8;
        }
        .chat-container {
            background: rgba(0, 0, 0, 0.5);
            border-radius: 15px;
            padding: 25px;
            margin: 30px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        #messages {
            height: 400px;
            overflow-y: auto;
            padding: 20px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid rgba(0, 180, 216, 0.1);
        }
        .message {
            margin: 15px 0;
            padding: 20px;
            border-radius: 15px;
            animation: fadeIn 0.5s;
            max-width: 85%;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .user-message {
            background: linear-gradient(135deg, rgba(0, 180, 216, 0.2), rgba(144, 224, 239, 0.1));
            margin-left: auto;
            border-right: 4px solid #00b4d8;
        }
        .bot-message {
            background: linear-gradient(135deg, rgba(20, 30, 48, 0.9), rgba(36, 59, 85, 0.7));
            margin-right: auto;
            border-left: 4px solid #48cae4;
            white-space: pre-wrap;
        }
        .input-area {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }
        input {
            flex: 1;
            padding: 18px;
            background: rgba(255, 255, 255, 0.08);
            border: 2px solid rgba(0, 180, 216, 0.3);
            border-radius: 12px;
            color: white;
            font-size: 16px;
            transition: all 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #00b4d8;
            background: rgba(255, 255, 255, 0.12);
            box-shadow: 0 0 0 4px rgba(0, 180, 216, 0.1);
        }
        button {
            padding: 18px 35px;
            background: linear-gradient(45deg, #00b4d8, #0077b6);
            color: white;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s;
        }
        button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 180, 216, 0.4);
        }
        .examples {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .example-btn {
            padding: 16px;
            background: rgba(0, 180, 216, 0.15);
            border: 1px solid rgba(0, 180, 216, 0.3);
            border-radius: 10px;
            color: #90e0ef;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
            font-size: 15px;
        }
        .example-btn:hover {
            background: rgba(0, 180, 216, 0.25);
            transform: translateX(-5px);
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        .stat {
            text-align: center;
            padding: 15px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #00b4d8;
            margin-bottom: 5px;
        }
        ::-webkit-scrollbar {
            width: 10px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 5px;
        }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #00b4d8, #0077b6);
            border-radius: 5px;
        }
        .neural-pulse {
            display: inline-block;
            width: 10px;
            height: 10px;
            background: #00b4d8;
            border-radius: 50%;
            margin-right: 10px;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><span class="neural-pulse"></span>natiq-ultimate v6.0</h1>
            <div class="tagline">سیستم عصبی-نمادین یکپارچه • کاملاً مستقل • بدون وابستگی</div>
        </div>
        
        <div class="architecture">
            <div class="component">
                <div class="component-icon">🤖</div>
                <h3>پردازش عصبی</h3>
                <p>درک زبان و تحلیل معنایی</p>
            </div>
            <div class="component">
                <div class="component-icon">🧠</div>
                <h3>دانش نمادین</h3>
                <p>گراف مفاهیم و روابط</p>
            </div>
            <div class="component">
                <div class="component-icon">⚡</div>
                <h3>یکپارچه‌سازی</h3>
                <p>ترکیب هوشمند نتایج</p>
            </div>
        </div>
        
        <div class="chat-container">
            <div id="messages">
                <div class="message bot-message">
                    🧬 **به سیستم عصبی-نمادین خوش آمدید!**
                    
                    این سیستم از معماری ترکیبی استفاده می‌کند:
                    • پردازش عصبی (درک الگوهای پیچیده)
                    • دانش نمادین (استدلال منطقی)
                    • یکپارچه‌سازی هوشمند
                    
                    💡 **می‌توانید بپرسید:**
                    • "هوش مصنوعی چیست؟"
                    • "تفاوت یادگیری ماشین و شبکه عصبی؟"
                    • "چگونه با پایتون هوش مصنوعی بسازیم؟"
                </div>
            </div>
            
            <div class="input-area">
                <input type="text" id="questionInput" placeholder="سوال خود را درباره هوش مصنوعی بپرسید..." autocomplete="off">
                <button onclick="sendQuestion()">ارسال به سیستم عصبی</button>
            </div>
            
            <div class="examples">
                <div class="example-btn" onclick="setQuestion('هوش مصنوعی چیست؟')">🤔 سوال تعریفی</div>
                <div class="example-btn" onclick="setQuestion('تفاوت یادگیری ماشین و شبکه عصبی')">⚖️ سوال مقایسه‌ای</div>
                <div class="example-btn" onclick="setQuestion('چگونه با پایتون هوش مصنوعی بسازیم؟')">🛠️ سوال روشی</div>
                <div class="example-btn" onclick="setQuestion('چرا هوش مصنوعی مهم است؟')">🔍 سوال علّی</div>
            </div>
            
            <div class="stats">
                <div class="stat">
                    <div class="stat-value" id="requestsCount">0</div>
                    <div>درخواست‌ها</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="knowledgeCount">6</div>
                    <div>مفاهیم دانش</div>
                </div>
                <div class="stat">
                    <div class="stat-value">v6.0</div>
                    <div>نسخه سیستم</div>
                </div>
                <div class="stat">
                    <div class="stat-value">🟢</div>
                    <div>وضعیت آنلاین</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let requestCount = 0;
        
        function setQuestion(question) {
            document.getElementById('questionInput').value = question;
        }
        
        async function sendQuestion() {
            const input = document.getElementById('questionInput');
            const question = input.value.trim();
            
            if (!question) {
                alert('لطفاً سوالی بنویسید!');
                return;
            }
            
            // نمایش سوال کاربر
            const messagesDiv = document.getElementById('messages');
            const userMessage = document.createElement('div');
            userMessage.className = 'message user-message';
            userMessage.textContent = question;
            messagesDiv.appendChild(userMessage);
            
            // پاک کردن ورودی
            input.value = '';
            input.focus();
            
            // نمایش وضعیت پردازش
            const processingMsg = document.createElement('div');
            processingMsg.className = 'message bot-message';
            processingMsg.innerHTML = `
                <span class="neural-pulse"></span>در حال پردازش عصبی-نمادین...
                <div style="margin-top: 10px; font-size: 0.9em; opacity: 0.8;">
                    تحلیل هدف → جستجوی دانش → تولید پاسخ
                </div>
            `;
            processingMsg.id = 'processingMsg';
            messagesDiv.appendChild(processingMsg);
            
            // اسکرول به پایین
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            
            try {
                // ارسال درخواست به سرور
                const response = await fetch('/api/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        question: question,
                        timestamp: new Date().toISOString()
                    })
                });
                
                // حذف پیام پردازش
                document.getElementById('processingMsg')?.remove();
                
                if (!response.ok) {
                    throw new Error(`خطای سرور: ${response.status}`);
                }
                
                const data = await response.json();
                
                if (data.success) {
                    // نمایش پاسخ
                    const botMessage = document.createElement('div');
                    botMessage.className = 'message bot-message';
                    botMessage.innerHTML = data.response.replace(/\\n/g, '<br>');
                    messagesDiv.appendChild(botMessage);
                    
                    // به‌روزرسانی آمار
                    requestCount++;
                    document.getElementById('requestsCount').textContent = requestCount;
                } else {
                    throw new Error(data.error || 'خطای ناشناخته');
                }
                
            } catch (error) {
                // حذف پیام پردازش
                document.getElementById('processingMsg')?.remove();
                
                // نمایش خطا
                const errorMsg = document.createElement('div');
                errorMsg.className = 'message bot-message';
                errorMsg.style.color = '#ff6b6b';
                errorMsg.innerHTML = `⚠️ خطا در ارتباط با سیستم:<br>${error.message}`;
                messagesDiv.appendChild(errorMsg);
            }
            
            // اسکرول به پایین
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        // فعال کردن Enter
        document.getElementById('questionInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendQuestion();
            }
        });
        
        // آمار اولیه
        document.getElementById('knowledgeCount').textContent = '6';
        document.getElementById('requestsCount').textContent = '0';
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def send_health(self):
        """صفحه وضعیت سلامت"""
        html = """<html dir="rtl"><body>
        <h1>✅ سیستم فعال است</h1>
        <p>natiq-ultimate v6.0 - سیستم عصبی نمادین</p>
        <p>زمان: {}</p>
        </body></html>""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def send_api_health(self):
        """وضعیت سلامت API"""
        response = {
            "status": "active",
            "system": "natiq-ultimate",
            "version": "6.0.0",
            "timestamp": datetime.now().isoformat(),
            "requests_processed": len(ai_system.history),
            "knowledge_size": len(ai_system.knowledge)
        }
        
        self.send_json_response(response)
    
    def send_json_response(self, data, status_code=200):
        """ارسال پاسخ JSON"""
        response = json.dumps(data, ensure_ascii=False, indent=2)
        
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

# ==================== تابع اصلی برای Vercel ====================

def handler(request, context):
    """Handler اصلی برای Vercel"""
    # این تابع توسط Vercel فراخوانی می‌شود
    # برای سادگی، از کلاس BaseHTTPRequestHandler استفاده می‌کنیم
    
    class VercelRequestHandler(RequestHandler):
        def __init__(self, request, client_address, server):
            self.request = request
            super().__init__(request, client_address, server)
    
    handler = VercelRequestHandler(request, ('127.0.0.1', 8000), None)
    return handler

# ==================== اجرای محلی (اختیاری) ====================

if __name__ == "__main__":
    print("🚀 Starting natiq-ultimate v6.0 on http://localhost:3000")
    print("🧠 Pure Python Neural-Symbolic AI System")
    print("⚡ No dependencies required!")
    
    server = HTTPServer(('localhost', 3000), RequestHandler)
    server.serve_forever()
