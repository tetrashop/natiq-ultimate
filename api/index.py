from http.server import BaseHTTPRequestHandler
import json
import math
import random
import hashlib
from datetime import datetime
import urllib.parse

# ==================== سیستم هوش مصنوعی ====================

class NatiqAI:
    """سیستم هوش مصنوعی عصبی-نمادین"""
    
    def __init__(self):
        self.knowledge = {
            "هوش مصنوعی": {
                "definition": "شاخه‌ای از علوم کامپیوتر که به ساخت ماشین‌های هوشمند می‌پردازد",
                "examples": ["یادگیری ماشین", "پردازش زبان طبیعی", "بینایی ماشین"],
                "importance": "بسیار بالا"
            },
            "یادگیری ماشین": {
                "definition": "توانایی سیستم‌ها برای یادگیری از داده بدون برنامه‌نویسی صریح",
                "examples": ["شبکه عصبی", "درخت تصمیم"],
                "importance": "بالا"
            },
            "شبکه عصبی": {
                "definition": "مدل محاسباتی الهام گرفته از شبکه عصبی مغز",
                "examples": ["پرسپترون", "شبکه کانولوشن"],
                "importance": "بالا"
            },
            "پایتون": {
                "definition": "زبان برنامه‌نویسی سطح بالا، مفسری و همه‌منظوره",
                "examples": ["علم داده", "یادگیری ماشین", "توسعه وب"],
                "importance": "بسیار بالا"
            }
        }
        self.history = []
    
    def analyze_question(self, question):
        """تحلیل سوال"""
        question_lower = question.lower()
        
        # تشخیص نوع سوال
        if any(word in question_lower for word in ["چیست", "چیه", "تعریف", "منظور"]):
            q_type = "تعریفی"
        elif any(word in question_lower for word in ["تفاوت", "فرق", "مقایسه"]):
            q_type = "مقایسه‌ای"
        elif any(word in question_lower for word in ["چگونه", "چطور", "روش"]):
            q_type = "روشی"
        elif any(word in question_lower for word in ["چرا", "علت", "دلیل"]):
            q_type = "علّی"
        else:
            q_type = "عمومی"
        
        # یافتن مفاهیم مرتبط
        found_concepts = []
        for concept in self.knowledge:
            if concept.lower() in question_lower:
                found_concepts.append(concept)
        
        return {
            "type": q_type,
            "concepts": found_concepts,
            "confidence": min(0.8 + len(found_concepts) * 0.1, 0.95)
        }
    
    def generate_response(self, question, analysis):
        """تولید پاسخ"""
        response = ""
        
        if analysis["type"] == "تعریفی" and analysis["concepts"]:
            concept = analysis["concepts"][0]
            data = self.knowledge.get(concept, {})
            response = f"""📚 **تعریف {concept}**:

{data.get('definition', 'تعریف یافت نشد')}

💡 **مثال‌ها**: {', '.join(data.get('examples', []))}
⭐ **اهمیت**: {data.get('importance', 'متوسط')}

🧠 **تولید شده توسط**: سیستم عصبی-نمادین natiq-ultimate"""
        
        elif analysis["type"] == "مقایسه‌ای":
            response = f"""⚖️ **تحلیل مقایسه‌ای**:

🔍 **مفاهیم شناسایی شده**: {', '.join(analysis['concepts']) if analysis['concepts'] else 'هیچ'}

🤖 **روش کار سیستم**:
1. استخراج مفاهیم
2. تحلیل شباهت‌ها و تفاوت‌ها
3. تولید پاسخ ساختاریافته

⚡ **دقت تحلیل**: {analysis['confidence']:.2f}"""
        
        else:
            response = f"""🧠 **سیستم عصبی-نمادین natiq-ultimate**:

💡 **سوال شما**: "{question}"

🎯 **تحلیل**:
• نوع سوال: {analysis['type']}
• مفاهیم یافت شده: {len(analysis['concepts'])}
• اطمینان سیستم: {analysis['confidence']:.2f}

🔧 **قابلیت‌های سیستم**:
✅ تحلیل خودکار سوالات
✅ جستجو در دانش تخصصی
✅ تولید پاسخ‌های هوشمند
✅ رابط کاربری مدرن

📚 **موضوعات قابل پرسش**:
• هوش مصنوعی
• یادگیری ماشین
• شبکه عصبی
• برنامه‌نویسی پایتون"""
        
        # ذخیره در تاریخچه
        self.history.append({
            "question": question[:50],
            "type": analysis["type"],
            "time": datetime.now().strftime("%H:%M:%S")
        })
        
        return response

# ==================== Handler اصلی برای Vercel ====================

ai_system = NatiqAI()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """مدیریت درخواست‌های GET"""
        path = self.path.split('?')[0]  # حذف query parameters
        
        if path == '/':
            self.send_home_page()
        elif path == '/health':
            self.send_health()
        elif path == '/api/health':
            self.send_api_health()
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        """مدیریت درخواست‌های POST"""
        if self.path == '/api/ask':
            self.handle_ask()
        else:
            self.send_error(404, "Not Found")
    
    def send_home_page(self):
        """ارسال صفحه اصلی"""
        html = """<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 natiq-ultimate v6.0</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: system-ui, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 30px;
            border: 1px solid rgba(0,150,255,0.3);
        }
        .header {
            text-align: center;
            padding: 20px;
            border-bottom: 2px solid #0096ff;
            margin-bottom: 30px;
        }
        h1 {
            color: #00b4d8;
            margin-bottom: 10px;
        }
        .chat-box {
            height: 400px;
            overflow-y: auto;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .message {
            margin: 10px 0;
            padding: 15px;
            border-radius: 10px;
            max-width: 80%;
        }
        .user-message {
            background: rgba(0,150,255,0.2);
            margin-left: auto;
            border-right: 3px solid #0096ff;
        }
        .bot-message {
            background: rgba(100,100,255,0.15);
            margin-right: auto;
            border-left: 3px solid #6464ff;
            white-space: pre-wrap;
        }
        .input-area {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        input {
            flex: 1;
            padding: 15px;
            background: rgba(255,255,255,0.1);
            border: 2px solid #0096ff;
            border-radius: 8px;
            color: white;
            font-size: 16px;
        }
        button {
            padding: 15px 30px;
            background: #0096ff;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
        }
        .examples {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 10px;
            margin-top: 20px;
        }
        .example {
            padding: 12px;
            background: rgba(0,150,255,0.1);
            border-radius: 8px;
            cursor: pointer;
            text-align: center;
            border: 1px solid rgba(0,150,255,0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 natiq-ultimate v6.0</h1>
            <p>سیستم عصبی-نمادین - نسخه پایدار</p>
        </div>
        
        <div class="chat-box" id="chatBox">
            <div class="message bot-message">
                به سیستم هوش مصنوعی عصبی-نمادین خوش آمدید!
                
                💡 می‌توانید سوالاتی مانند:
                • "هوش مصنوعی چیست؟"
                • "یادگیری ماشین چیست؟"
                • "تفاوت AI و ML چیست؟"
                
                را بپرسید.
            </div>
        </div>
        
        <div class="input-area">
            <input type="text" id="questionInput" placeholder="سوال خود را بنویسید...">
            <button onclick="sendQuestion()">ارسال</button>
        </div>
        
        <div class="examples">
            <div class="example" onclick="setQuestion('هوش مصنوعی چیست؟')">هوش مصنوعی چیست؟</div>
            <div class="example" onclick="setQuestion('یادگیری ماشین چیست؟')">یادگیری ماشین چیست؟</div>
            <div class="example" onclick="setQuestion('تفاوت AI و ML چیست؟')">تفاوت AI و ML</div>
            <div class="example" onclick="setQuestion('شبکه عصبی چیست؟')">شبکه عصبی چیست؟</div>
        </div>
    </div>
    
    <script>
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
            const chatBox = document.getElementById('chatBox');
            const userMsg = document.createElement('div');
            userMsg.className = 'message user-message';
            userMsg.textContent = question;
            chatBox.appendChild(userMsg);
            
            input.value = '';
            
            try {
                const response = await fetch('/api/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ question: question })
                });
                
                const data = await response.json();
                
                // نمایش پاسخ
                const botMsg = document.createElement('div');
                botMsg.className = 'message bot-message';
                botMsg.innerHTML = data.response.replace(/\\n/g, '<br>');
                chatBox.appendChild(botMsg);
                
                chatBox.scrollTop = chatBox.scrollHeight;
                
            } catch (error) {
                const errorMsg = document.createElement('div');
                errorMsg.className = 'message bot-message';
                errorMsg.textContent = 'خطا در ارتباط با سرور';
                chatBox.appendChild(errorMsg);
            }
        }
        
        // فعال کردن Enter
        document.getElementById('questionInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendQuestion();
            }
        });
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def handle_ask(self):
        """مدیریت سوالات"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data) if post_data else {}
            
            question = data.get('question', '').strip()
            
            if not question:
                response = {
                    "success": False,
                    "error": "سوال نمی‌تواند خالی باشد"
                }
                self.send_json_response(response, 400)
            else:
                # پردازش سوال
                analysis = ai_system.analyze_question(question)
                response_text = ai_system.generate_response(question, analysis)
                
                result = {
                    "success": True,
                    "question": question,
                    "response": response_text,
                    "analysis": analysis,
                    "timestamp": datetime.now().isoformat()
                }
                self.send_json_response(result)
                
        except Exception as e:
            response = {
                "success": False,
                "error": str(e)
            }
            self.send_json_response(response, 500)
    
    def send_health(self):
        """صفحه سلامت"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'<html><body><h1>✅ سیستم فعال است</h1></body></html>')
    
    def send_api_health(self):
        """وضعیت API"""
        response = {
            "status": "active",
            "system": "natiq-ultimate",
            "version": "6.0.0",
            "timestamp": datetime.now().isoformat()
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
    
    def send_error(self, code, message):
        """ارسال خطا"""
        self.send_response(code)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(f"{code} {message}".encode('utf-8'))

# ==================== تابع اصلی برای Vercel ====================

# این تابع توسط Vercel فراخوانی می‌شود
def handler(request, context):
    """Handler اصلی برای Vercel Serverless Functions"""
    import sys
    import io
    
    # ساخت request object برای BaseHTTPRequestHandler
    class Request:
        def __init__(self, method, path, headers, body):
            self.method = method
            self.path = path
            self.headers = headers
            self.body = body
            self.wfile = io.BytesIO()
            self.rfile = io.BytesIO(body.encode() if body else b'')
    
    # ساخت response object
    class Response:
        def __init__(self):
            self.status_code = 200
            self.headers = {}
            self.body = b''
    
    # ایجاد Handler
    req = Request(
        method=request.get('httpMethod', 'GET'),
        path=request.get('path', '/'),
        headers=request.get('headers', {}),
        body=request.get('body', '')
    )
    
    handler_obj = Handler(req, ('127.0.0.1', 8000), None)
    
    # خواندن پاسخ
    response_body = handler_obj.wfile.getvalue()
    
    return {
        'statusCode': handler_obj.status_code,
        'headers': dict(handler_obj.headers),
        'body': response_body.decode('utf-8')
    }

# راه‌اندازی ساده برای Vercel
def lambda_handler(event, context):
    """Handler سازگار با AWS Lambda (Vercel از این فرمت پشتیبانی می‌کند)"""
    return handler(event, context)

# اگر فایل مستقیماً اجرا شود (برای تست محلی)
if __name__ == "__main__":
    from http.server import HTTPServer
    print("🚀 Starting server on http://localhost:3000")
    server = HTTPServer(('localhost', 3000), Handler)
    server.serve_forever()
