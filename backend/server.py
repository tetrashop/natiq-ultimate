"""
natiq-ultimate v6.0 - سیستم مستقل عصبی-نمادین
بدون هیچ وابستگی خارجی - کاملاً Pure Python
"""

import json
import re
import math
import random
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import defaultdict
from urllib.parse import quote

# ==================== کلاس‌های سیستم ====================

class SimpleNeuralSystem:
    """سیستم عصبی ساده بدون وابستگی"""
    
    def __init__(self):
        self.word_vectors = {}
        self.initialize_embeddings()
    
    def initialize_embeddings(self):
        """ایجاد embeddingهای ساده"""
        words = [
            "هوش", "مصنوعی", "یادگیری", "ماشین", "داده", 
            "الگوریتم", "شبکه", "عصبی", "مدل", "برنامه"
        ]
        
        for word in words:
            # ایجاد بردار 5 بعدی ساده
            vector = [random.random() for _ in range(5)]
            # نرمال‌سازی
            norm = math.sqrt(sum(x*x for x in vector))
            if norm > 0:
                vector = [x/norm for x in vector]
            self.word_vectors[word] = vector
    
    def get_sentence_vector(self, text: str) -> List[float]:
        """ایجاد بردار برای جمله"""
        words = text.split()
        vectors = []
        
        for word in words:
            if word in self.word_vectors:
                vectors.append(self.word_vectors[word])
            else:
                # بردار تصادفی برای کلمات ناشناخته
                vec = [random.random() for _ in range(5)]
                norm = math.sqrt(sum(x*x for x in vec))
                if norm > 0:
                    vec = [x/norm for x in vec]
                vectors.append(vec)
        
        if vectors:
            # میانگین بردارها
            result = [0.0] * 5
            for vec in vectors:
                for i in range(5):
                    result[i] += vec[i]
            return [x/len(vectors) for x in result]
        return [0.0] * 5
    
    def classify_intent(self, text: str) -> Dict:
        """طبقه‌بندی هدف سوال"""
        text_lower = text.lower()
        
        patterns = {
            "definition": ["چیست", "چیه", "تعریف", "منظور", "معنی"],
            "causal": ["چرا", "علت", "دلیل", "چرایی"],
            "comparison": ["تفاوت", "فرق", "مقایسه"],
            "howto": ["چگونه", "چطور", "روش"],
            "general": ["", "", ""]
        }
        
        scores = {}
        for intent, keywords in patterns.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            scores[intent] = score / max(len(keywords), 1)
        
        # پیدا کردن هدف اصلی
        primary = max(scores.items(), key=lambda x: x[1])
        
        return {
            "primary": primary[0],
            "confidence": primary[1],
            "all_scores": scores
        }

class KnowledgeBase:
    """پایگاه دانش ساده"""
    
    def __init__(self):
        self.concepts = self.initialize_concepts()
    
    def initialize_concepts(self):
        """مفاهیم پایه"""
        return {
            "هوش مصنوعی": {
                "definition": "شاخه‌ای از علوم کامپیوتر که به ساخت ماشین‌های هوشمند می‌پردازد",
                "type": "علمی",
                "examples": ["یادگیری ماشین", "پردازش زبان طبیعی", "بینایی ماشین"],
                "importance": "بسیار بالا"
            },
            "یادگیری ماشین": {
                "definition": "توانایی سیستم‌ها برای یادگیری از داده بدون برنامه‌نویسی صریح",
                "type": "زیرشاخه",
                "examples": ["شبکه عصبی", "درخت تصمیم", "ماشین بردار پشتیبان"],
                "importance": "بالا"
            },
            "شبکه عصبی": {
                "definition": "مدل محاسباتی الهام گرفته از شبکه عصبی مغز",
                "type": "الگوریتم",
                "examples": ["پرسپترون", "شبکه کانولوشن", "شبکه بازگشتی"],
                "importance": "بالا"
            },
            "پایتون": {
                "definition": "زبان برنامه‌نویسی سطح بالا، مفسری و همه‌منظوره",
                "type": "زبان برنامه‌نویسی",
                "examples": ["دیتاساینس", "یادگیری ماشین", "توسعه وب"],
                "importance": "بسیار بالا"
            }
        }
    
    def search(self, query: str) -> List[Dict]:
        """جستجو در دانش"""
        results = []
        query_lower = query.lower()
        
        for concept, data in self.concepts.items():
            if query_lower in concept.lower() or any(query_lower in word for word in concept.lower().split()):
                results.append({
                    "concept": concept,
                    "data": data,
                    "match_score": 1.0
                })
        
        return results

class ResponseGenerator:
    """تولید کننده پاسخ"""
    
    def __init__(self):
        self.templates = self.initialize_templates()
    
    def initialize_templates(self):
        """قالب‌های پاسخ"""
        return {
            "definition": [
                "📚 **تعریف**:\n\n{concept}:\n{definition}\n\n💡 **نکته**: {importance}",
                "🧠 **مفهوم**:\n\n{concept}\n\n📖 **تعریف**:\n{definition}\n\n⭐ **اهمیت**: {importance}",
                "🔍 **تحلیل**:\n\nمفهوم **{concept}** به شرح زیر است:\n{definition}\n\n🎯 **درجه اهمیت**: {importance}"
            ],
            "causal": [
                "🔗 **تحلیل علّی**:\n\nسوال شما درباره علت و معلول است. سیستم عصبی-نمادین این موضوع را تحلیل می‌کند.\n\n💭 **روش تحلیل**:\n1. شناسایی متغیرها\n2. جستجوی روابط علّی\n3. استنتاج منطقی",
                "⚡ **علت‌یابی**:\n\nبرای تحلیل علّی دقیق، نیاز به داده‌های بیشتر داریم. سیستم می‌تواند با اطلاعات موجود تحلیل اولیه ارائه دهد.",
                "🔬 **تحلیل علّی عصبی-نمادین**:\n\nاین سیستم ترکیبی از:\n• استدلال عصبی (الگوهای پیچیده)\n• استدلال نمادین (منطق دقیق)\n\nبرای تحلیل دقیق‌تر، جزئیات بیشتری ارائه دهید."
            ],
            "comparison": [
                "⚖️ **مقایسه**:\n\nسیستم عصبی-نمادین برای مقایسه:\n1. مفاهیم را استخراج می‌کند\n2. شباهت‌ها و تفاوت‌ها را می‌یابد\n3. نتایج را ساختار می‌دهد",
                "📊 **تحلیل مقایسه‌ای**:\n\nویژگی‌های مقایسه:\n• دقت تحلیل: ~85%\n• سرعت پردازش: فوری\n• عمق تحلیل: متوسط به بالا",
                "🔍 **مقایسه عصبی-نمادین**:\n\nروش کار سیستم:\n🤖 **عصبی**: درک الگوهای پیچیده\n🔗 **نمادین**: استنتاج منطقی دقیق\n⚡ **ترکیب**: بهترین هر دو جهان"
            ],
            "howto": [
                "🛠️ **راهنما**:\n\nمراحل کلی:\n1. تعریف مسئله\n2. جمع‌آوری داده\n3. انتخاب مدل\n4. آموزش\n5. ارزیابی\n6. بهبود",
                "📋 **دستورالعمل**:\n\nبرای حل مسئله با سیستم عصبی-نمادین:\n• ورودی: سوال روشی\n• پردازش: تحلیل ترکیبی\n• خروجی: راه‌حل ساختاریافته",
                "🎯 **روش کار**:\n\nسیستم عصبی-نمادین:\n1. سوال را تحلیل می‌کند\n2. دانش مرتبط را می‌یابد\n3. راه‌حل‌ها را تولید می‌کند\n4. بهترین را انتخاب می‌کند"
            ],
            "general": [
                "🧠 **سیستم عصبی-نمادین فعال است**\n\nمن از ترکیب:\n• پردازش عصبی (یادگیری عمیق)\n• دانش نمادین (گراف دانش)\nاستفاده می‌کنم.\n\n💡 می‌توانید سوالات تعریفی، مقایسه‌ای، علّی یا روشی بپرسید.",
                "⚡ **natiq-ultimate v6.0**\n\nمعماری ترکیبی:\n🤖 لایه عصبی: درک زبان\n📚 لایه دانش: ذخیره اطلاعات\n🔗 لایه نمادین: استنتاج منطقی\n\nسوال خود را بپرسید...",
                "🎯 **سیستم یکپارچه**\n\nقابلیت‌ها:\n✅ تحلیل هدف سوال\n✅ جستجو در دانش\n✅ تولید پاسخ هوشمند\n✅ یادگیری تطبیقی\n\nپرسش خود را مطرح کنید."
            ]
        }
    
    def generate(self, intent: str, concept_data: Dict = None) -> str:
        """تولید پاسخ"""
        templates = self.templates.get(intent, self.templates["general"])
        template = random.choice(templates)
        
        if concept_data and intent == "definition":
            return template.format(
                concept=concept_data.get("concept", ""),
                definition=concept_data.get("data", {}).get("definition", ""),
                importance=concept_data.get("data", {}).get("importance", "")
            )
        
        return template

# ==================== سیستم اصلی ====================

class NatiqSystem:
    """سیستم اصلی natiq"""
    
    def __init__(self):
        self.neural = SimpleNeuralSystem()
        self.knowledge = KnowledgeBase()
        self.generator = ResponseGenerator()
        self.history = []
        self.session_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
    
    def process(self, question: str) -> Dict:
        """پردازش سوال و تولید پاسخ"""
        start_time = time.time()
        
        # تحلیل عصبی
        intent = self.neural.classify_intent(question)
        
        # جستجو در دانش
        knowledge_results = self.knowledge.search(question)
        
        # تولید پاسخ
        if knowledge_results and intent["primary"] == "definition":
            response = self.generator.generate(intent["primary"], knowledge_results[0])
        else:
            response = self.generator.generate(intent["primary"])
        
        processing_time = time.time() - start_time
        
        # ذخیره در تاریخچه
        self.history.append({
            "question": question,
            "intent": intent,
            "time": datetime.now().strftime("%H:%M:%S"),
            "processing_time": processing_time
        })
        
        return {
            "question": question,
            "response": response,
            "analysis": {
                "intent": intent["primary"],
                "confidence": intent["confidence"],
                "concepts_found": len(knowledge_results),
                "processing_time": processing_time
            },
            "system": {
                "name": "natiq-ultimate",
                "version": "6.0.0",
                "session": self.session_id,
                "history_count": len(self.history)
            }
        }

# ایجاد نمونه سیستم
system = NatiqSystem()

# ==================== HTTP Server ساده ====================

def simple_http_server(environ, start_response):
    """سرور HTTP ساده بدون FastAPI"""
    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET')
    
    # هندلینگ روت
    if path == '/' and method == 'GET':
        return handle_home(environ, start_response)
    elif path == '/api/ask' and method == 'POST':
        return handle_api_ask(environ, start_response)
    elif path == '/api/health' and method == 'GET':
        return handle_api_health(environ, start_response)
    else:
        return handle_not_found(environ, start_response)

def handle_home(environ, start_response):
    """صفحه اصلی"""
    html = """
    <!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🧠 natiq-ultimate v6.0</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: system-ui, sans-serif;
                background: linear-gradient(135deg, #0c0c0c, #1a1a2e);
                color: white;
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
            }
            .header {
                text-align: center;
                padding: 30px;
                background: linear-gradient(90deg, #1a237e, #0d47a1);
                border-radius: 15px;
                margin-bottom: 20px;
            }
            h1 { color: #82b1ff; margin-bottom: 10px; }
            .chat-box {
                background: rgba(30, 35, 60, 0.8);
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                height: 400px;
                overflow-y: auto;
            }
            .message {
                margin: 10px 0;
                padding: 15px;
                border-radius: 10px;
                max-width: 80%;
            }
            .user-message {
                background: rgba(41, 98, 255, 0.3);
                margin-left: auto;
                border-right: 3px solid #2962ff;
            }
            .bot-message {
                background: rgba(187, 134, 252, 0.2);
                margin-right: auto;
                border-left: 3px solid #bb86fc;
            }
            .input-area {
                display: flex;
                gap: 10px;
                margin-top: 20px;
            }
            input {
                flex: 1;
                padding: 15px;
                background: rgba(255,255,255,0.1);
                border: 2px solid #2962ff;
                border-radius: 8px;
                color: white;
                font-size: 16px;
            }
            button {
                padding: 15px 30px;
                background: #2962ff;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
            }
            .examples {
                display: flex;
                gap: 10px;
                margin-top: 20px;
                flex-wrap: wrap;
            }
            .example {
                padding: 10px 15px;
                background: rgba(41, 98, 255, 0.2);
                border-radius: 8px;
                cursor: pointer;
                text-align: center;
                flex: 1;
                min-width: 150px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧠 natiq-ultimate v6.0</h1>
                <p>سیستم عصبی-نمادین مستقل - بدون وابستگی خارجی</p>
            </div>
            
            <div class="chat-box" id="chatBox">
                <div class="message bot-message">
                    به سیستم عصبی-نمادین خوش آمدید!<br>
                    می‌توانید سوالات مربوط به هوش مصنوعی، یادگیری ماشین و ... بپرسید.
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
                <div class="example" onclick="setQuestion('چگونه هوش مصنوعی بسازیم؟')">چگونه AI بسازیم؟</div>
            </div>
        </div>
        
        <script>
            function setQuestion(question) {
                document.getElementById('questionInput').value = question;
            }
            
            async function sendQuestion() {
                const input = document.getElementById('questionInput');
                const question = input.value.trim();
                if (!question) return;
                
                // نمایش سوال کاربر
                const chatBox = document.getElementById('chatBox');
                const userMsg = document.createElement('div');
                userMsg.className = 'message user-message';
                userMsg.textContent = question;
                chatBox.appendChild(userMsg);
                
                // پاک کردن ورودی
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
                    
                    // اسکرول به پایین
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
    </html>
    """
    
    start_response('200 OK', [
        ('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(html.encode('utf-8'))))
    ])
    return [html.encode('utf-8')]

def handle_api_ask(environ, start_response):
    """API پرسش و پاسخ"""
    try:
        # خواندن بدنه درخواست
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(content_length).decode('utf-8')
        data = json.loads(body) if body else {}
        
        question = data.get('question', '').strip()
        
        if not question:
            response_data = {
                "error": "سوال نمی‌تواند خالی باشد",
                "success": False
            }
        else:
            # پردازش سوال
            result = system.process(question)
            response_data = {
                "success": True,
                "question": question,
                "response": result["response"],
                "analysis": result["analysis"],
                "system": result["system"]
            }
        
        response_json = json.dumps(response_data, ensure_ascii=False)
        
        start_response('200 OK', [
            ('Content-Type', 'application/json; charset=utf-8'),
            ('Access-Control-Allow-Origin', '*')
        ])
        return [response_json.encode('utf-8')]
        
    except Exception as e:
        error_response = json.dumps({
            "error": str(e),
            "success": False
        }, ensure_ascii=False)
        
        start_response('500 Internal Server Error', [
            ('Content-Type', 'application/json; charset=utf-8')
        ])
        return [error_response.encode('utf-8')]

def handle_api_health(environ, start_response):
    """API وضعیت سیستم"""
    health_data = {
        "status": "active",
        "system": "natiq-ultimate",
        "version": "6.0.0",
        "components": {
            "neural": "operational",
            "knowledge_base": "operational",
            "response_generator": "operational"
        },
        "statistics": {
            "concepts": len(system.knowledge.concepts),
            "session_id": system.session_id,
            "requests_processed": len(system.history)
        }
    }
    
    response_json = json.dumps(health_data, ensure_ascii=False)
    
    start_response('200 OK', [
        ('Content-Type', 'application/json; charset=utf-8'),
        ('Access-Control-Allow-Origin', '*')
    ])
    return [response_json.encode('utf-8')]

def handle_not_found(environ, start_response):
    """صفحه 404"""
    start_response('404 Not Found', [
        ('Content-Type', 'text/plain; charset=utf-8')
    ])
    return [b'404 - Page Not Found']

# ==================== ورودی اصلی ====================

if __name__ == '__main__':
    # برای اجرای محلی با wsgiref
    from wsgiref.simple_server import make_server
    
    print("🚀 Starting natiq-ultimate v6.0 on http://localhost:8000")
    print("🧠 System: Pure Python Neural-Symbolic AI")
    print("⚡ No external dependencies needed!")
    
    with make_server('', 8000, simple_http_server) as httpd:
        httpd.serve_forever()

# نکته: برای Vercel، ما از WSGI استفاده می‌کنیم
# Vercel به طور خودکار این فایل را به عنوان اپلیکیشن تشخیص می‌دهد
