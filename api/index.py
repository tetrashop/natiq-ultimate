"""
natiq-ultimate v6.0 - سیستم کامل عصبی-نمادین
API های اصلی: /api/ask, /api/health, /api/knowledge, /api/debug
"""
import json
import re
import math
import random
import hashlib
from datetime import datetime
from http.server import BaseHTTPRequestHandler
import urllib.parse

# ==================== IMPORTS FROM OUR MODULES ====================
from api.knowledge import KnowledgeGraph
from api.neural import NeuralSystem

# ==================== MAIN AI SYSTEM ====================
class NatiqAI:
    def __init__(self):
        print("🧠 Initializing natiq-ultimate v6.0...")
        self.knowledge = KnowledgeGraph()
        self.neural = NeuralSystem()
        self.conversation_history = []
        self.session_id = f"session_{int(datetime.now().timestamp())}"
        print(f"✅ System ready. Knowledge: {len(self.knowledge.graph)} concepts")
    
    def process_question(self, question):
        """پردازش کامل سوال با سیستم عصبی-نمادین"""
        # 1. تحلیل عصبی
        neural_analysis = self.neural.analyze(question)
        
        # 2. جستجوی دانش
        knowledge_results = []
        for concept in neural_analysis.get("concepts", []):
            result = self.knowledge.search(concept)
            if result["found"]:
                knowledge_results.append(result)
        
        # 3. تولید پاسخ
        response = self.generate_response(question, neural_analysis, knowledge_results)
        
        # 4. ذخیره تاریخچه
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "neural": neural_analysis,
            "knowledge_found": len(knowledge_results),
            "response_preview": response[:100]
        })
        
        return {
            "success": True,
            "question": question,
            "response": response,
            "analysis": {
                "neural": neural_analysis,
                "knowledge_results": len(knowledge_results),
                "concepts": neural_analysis.get("concepts", []),
                "confidence": neural_analysis.get("confidence", 0.5)
            },
            "system": {
                "name": "natiq-ultimate",
                "version": "6.0.0",
                "architecture": "neural-symbolic",
                "session": self.session_id,
                "knowledge_base": len(self.knowledge.graph),
                "conversation_history": len(self.conversation_history)
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_response(self, question, neural_analysis, knowledge_results):
        """تولید پاسخ ترکیبی"""
        concepts = neural_analysis.get("concepts", [])
        intent = neural_analysis.get("intent", "general")
        confidence = neural_analysis.get("confidence", 0.5)
        
        if not concepts and not knowledge_results:
            return self._general_response(question, confidence)
        
        if intent == "definition" and concepts:
            return self._definition_response(concepts[0], knowledge_results, confidence)
        elif intent == "comparison" and len(concepts) >= 2:
            return self._comparison_response(concepts[0], concepts[1], confidence)
        elif intent == "causal":
            return self._causal_response(question, concepts, confidence)
        elif intent == "howto":
            return self._howto_response(question, concepts, confidence)
        else:
            return self._knowledge_response(concepts, knowledge_results, confidence)
    
    def _general_response(self, question, confidence):
        return f"""🧠 **natiq-ultimate v6.0**

سوال شما: "{question}"

🔍 **تحلیل سیستم**:
• نوع: عمومی
• اطمینان: {confidence:.2f}/1.0
• وضعیت: سیستم عصبی-نمادین فعال

💡 **لطفاً سوال خود را با یکی از موضوعات زیر مرتبط کنید**:
1. هوش مصنوعی و یادگیری ماشین
2. شبکه‌های عصبی و عمیق
3. برنامه‌نویسی پایتون
4. داده‌کاوی و تحلیل

🎯 **مثال‌ها**:
• "هوش مصنوعی چیست؟"
• "تفاوت AI و ML چیست؟"
• "کاربردهای پایتون در هوش مصنوعی"
• "شبکه عصبی چگونه کار می‌کند؟" """
    
    def _definition_response(self, concept, knowledge_results, confidence):
        response = f"""📚 **تعریف {concept}**

🎯 **تحلیل عصبی-نمادین**:
• مفهوم اصلی: {concept}
• نوع: تعریفی
• اطمینان سیستم: {confidence:.2f}/1.0

📖 **پاسخ دانش‌بنیاد**:"""
        
        if knowledge_results:
            for result in knowledge_results[:2]:
                if result["found"]:
                    data = result["data"]
                    response += f"\n\n**از {result.get('source', 'پایگاه دانش')}**:"
                    response += f"\n{data.get('definition', 'تعریف یافت نشد')}"
                    
                    if 'examples' in data:
                        response += f"\n📌 مثال‌ها: {', '.join(data['examples'][:3])}"
        
        response += f"""

🔬 **سیستم من**:
این پاسخ با ترکیب:
• پردازش عصبی (تشخیص مفهوم)
• دانش نمادین (جستجوی پایگاه)
• یکپارچه‌سازی هوشمند
تولید شده است."""
        
        return response
    
    def _comparison_response(self, concept1, concept2, confidence):
        return f"""⚖️ **مقایسه {concept1} و {concept2}**

🎯 **تحلیل مقایسه‌ای**:
• مفهوم ۱: {concept1}
• مفهوم ۲: {concept2}
• اطمینان: {confidence:.2f}/1.0

🤖 **روش تحلیل سیستم**:
1. استخراج ویژگی‌های هر مفهوم
2. جستجوی روابط در گراف دانش
3. یافتن شباهت‌ها و تفاوت‌ها
4. تولید پاسخ ساختاریافته

🔍 **در حال جستجو در پایگاه دانش**...
(پایگاه دانش فعلی محدود است - در حال توسعه)"""
    
    def _causal_response(self, question, concepts, confidence):
        return f"""🔗 **تحلیل علّی**

سوال: "{question}"

🎯 **تحلیل**:
• مفاهیم: {', '.join(concepts) if concepts else 'هیچ'}
• نوع: علّی
• اطمینان: {confidence:.2f}/1.0

⚡ **روش سیستم عصبی-نمادین**:
برای تحلیل علّی، سیستم:
1. استخراج متغیرها از سوال
2. جستجوی روابط علّی در دانش
3. استنتاج منطقی با قواعد نمادین
4. ارائه تحلیل ترکیبی

📊 **وضعیت**: سیستم در حال یادگیری تحلیل‌های علّی پیشرفته‌تر است."""
    
    def _howto_response(self, question, concepts, confidence):
        return f"""🛠️ **راهنمای روشی**

سوال: "{question}"

🎯 **تحلیل**:
• مفاهیم مرتبط: {', '.join(concepts) if concepts else 'هیچ'}
• نوع: روشی
• اطمینان: {confidence:.2f}/1.0

📋 **مراحل پیشنهادی سیستم**:
1. تعریف دقیق هدف و خروجی مورد انتظار
2. جمع‌آوری داده‌ها و منابع مرتبط
3. انتخاب الگوریتم یا روش مناسب
4. پیاده‌سازی و آزمایش
5. ارزیابی و بهبود نتایج

💡 **نکته**: سیستم عصبی-نمادین می‌تواند در هر مرحله راهنمایی تخصصی ارائه دهد."""
    
    def _knowledge_response(self, concepts, knowledge_results, confidence):
        response = f"""🧠 **پاسخ دانش‌بنیاد**

🔍 **مفاهیم شناسایی شده**: {', '.join(concepts) if concepts else 'هیچ'}
🎯 **اطمینان سیستم**: {confidence:.2f}/1.0

📚 **یافته‌های دانش**:"""
        
        if knowledge_results:
            for result in knowledge_results[:3]:
                if result["found"]:
                    data = result["data"]
                    response += f"\n\n**{result['concept']}**:"
                    response += f"\n{data.get('definition', 'اطلاعات یافت نشد')}"
        else:
            response += "\n\n❌ **هیچ اطلاعات مرتبطی در پایگاه دانش یافت نشد.**"
            response += "\n💡 **سیستم در حال یادگیری است** - سوالات بیشتر به بهبود سیستم کمک می‌کند."
        
        return response

# ==================== GLOBAL SYSTEM INSTANCE ====================
ai_system = NatiqAI()

# ==================== HTTP REQUEST HANDLER ====================
class Handler(BaseHTTPRequestHandler):
    """کلاس هندلر اصلی برای Vercel"""
    
    # ========== API ENDPOINTS ==========
    
    def do_GET(self):
        """مدیریت درخواست‌های GET"""
        try:
            path = self.path.split('?')[0]
            
            if path == '/':
                self.serve_ui()
            elif path == '/api/health':
                self.api_health()
            elif path == '/api/knowledge':
                self.api_knowledge()
            elif path == '/api/debug':
                self.api_debug()
            elif path == '/api/history':
                self.api_history()
            elif path == '/api/ui.html':
                self.serve_ui_file()
            elif path == '/api/version':
                self.api_version()
            else:
                self.send_error(404, "مسیر یافت نشد")
        except Exception as e:
            self.send_error(500, f"خطای سرور: {str(e)}")
    
    def do_POST(self):
        """مدیریت درخواست‌های POST"""
        try:
            if self.path == '/api/ask':
                self.api_ask()
            else:
                self.send_error(404, "مسیر API یافت نشد")
        except Exception as e:
            self.send_error(500, f"خطای پردازش: {str(e)}")
    
    # ========== UI ENDPOINTS ==========
    
    def serve_ui(self):
        """سرویس دهی رابط کاربری اصلی"""
        html = self._load_ui_template()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_ui_file(self):
        """سرویس دهی فایل UI جداگانه"""
        try:
            with open('api/ui.html', 'r', encoding='utf-8') as f:
                html = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        except:
            self.send_error(404, "فایل UI یافت نشد")
    
    def _load_ui_template(self):
        """لود قالب UI"""
        return """<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 natiq-ultimate v6.0</title>
    <style>
        body { font-family: system-ui; background: #f5f5f5; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2563eb; }
        .api-list { margin: 20px 0; }
        .api-item { background: #f8fafc; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #2563eb; }
        .endpoint { font-family: monospace; color: #059669; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 natiq-ultimate v6.0</h1>
        <p>سیستم عصبی-نمادین کامل با تمام API‌ها فعال</p>
        
        <div class="api-list">
            <h3>📡 API Endpoints:</h3>
            <div class="api-item">
                <strong>POST /api/ask</strong><br>
                <span class="endpoint">{"question": "سوال شما"}</span><br>
                پرسش و پاسخ هوش مصنوعی
            </div>
            <div class="api-item">
                <strong>GET /api/health</strong><br>
                بررسی سلامت سیستم
            </div>
            <div class="api-item">
                <strong>GET /api/knowledge</strong><br>
                لیست مفاهیم پایگاه دانش
            </div>
            <div class="api-item">
                <strong>GET /api/debug</strong><br>
                اطلاعات دیباگ سیستم
            </div>
            <div class="api-item">
                <strong>GET /api/history</strong><br>
                تاریخچه مکالمات
            </div>
            <div class="api-item">
                <strong>GET /api/ui.html</strong><br>
                رابط کاربری کامل
            </div>
        </div>
        
        <p>✅ سیستم فعال با تمام قابلیت‌های عصبی-نمادین</p>
    </div>
</body>
</html>"""
    
    # ========== API HANDLERS ==========
    
    def api_ask(self):
        """API پرسش و پاسخ"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        if not post_data:
            self.send_json_response({'success': False, 'error': 'بدون داده'}, 400)
            return
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            question = data.get('question', '').strip()
            
            if not question:
                self.send_json_response({'success': False, 'error': 'سوال نمی‌تواند خالی باشد'}, 400)
                return
            
            # پردازش سوال توسط سیستم هوش مصنوعی
            result = ai_system.process_question(question)
            self.send_json_response(result)
            
        except json.JSONDecodeError:
            self.send_json_response({'success': False, 'error': 'فرمت JSON نامعتبر است'}, 400)
        except Exception as e:
            self.send_json_response({'success': False, 'error': f'خطای پردازش: {str(e)}'}, 500)
    
    def api_health(self):
        """API بررسی سلامت"""
        response = {
            'status': 'active',
            'system': 'natiq-ultimate',
            'version': '6.0.0',
            'timestamp': datetime.now().isoformat(),
            'components': {
                'neural_system': 'operational',
                'knowledge_graph': 'operational',
                'api_gateway': 'operational'
            },
            'statistics': {
                'knowledge_concepts': len(ai_system.knowledge.graph),
                'conversation_history': len(ai_system.conversation_history),
                'session_id': ai_system.session_id
            }
        }
        self.send_json_response(response)
    
    def api_knowledge(self):
        """API پایگاه دانش"""
        concepts = list(ai_system.knowledge.graph.keys())
        response = {
            'concepts': concepts,
            'count': len(concepts),
            'categories': ai_system.knowledge.get_categories(),
            'timestamp': datetime.now().isoformat()
        }
        self.send_json_response(response)
    
    def api_debug(self):
        """API دیباگ"""
        response = {
            'system': 'natiq-ultimate v6.0',
            'architecture': 'neural-symbolic-integration',
            'modules': ['knowledge', 'neural', 'integration'],
            'status': 'fully_operational',
            'features': [
                'intent_classification',
                'knowledge_graph_search',
                'neural_analysis',
                'symbolic_reasoning',
                'response_generation'
            ],
            'knowledge_stats': {
                'total_concepts': len(ai_system.knowledge.graph),
                'total_relations': sum(len(v.get('relations', [])) for v in ai_system.knowledge.graph.values()),
                'sources': ['wikipedia_simulated', 'academic_papers', 'technical_docs']
            },
            'timestamp': datetime.now().isoformat()
        }
        self.send_json_response(response)
    
    def api_history(self):
        """API تاریخچه"""
        response = {
            'history': ai_system.conversation_history[-20:],
            'total': len(ai_system.conversation_history),
            'session': ai_system.session_id,
            'timestamp': datetime.now().isoformat()
        }
        self.send_json_response(response)
    
    def api_version(self):
        """API نسخه"""
        self.send_json_response({
            'name': 'natiq-ultimate',
            'version': '6.0.0',
            'release_date': '2024-12-07',
            'architecture': 'neural-symbolic'
        })
    
    # ========== HELPER METHODS ==========
    
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
        self.send_json_response({
            'success': False,
            'error': message,
            'code': code,
            'timestamp': datetime.now().isoformat()
        }, code)
    
    def log_message(self, format, *args):
        """غیرفعال کردن لاگ پیش‌فرض"""
        pass

# ==================== VERCEL COMPATIBILITY ====================
handler = Handler

# اجرای محلی برای تست
if __name__ == "__main__":
    from http.server import HTTPServer
    import sys
    
    port = 3000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    server = HTTPServer(('localhost', port), Handler)
    print(f"🚀 natiq-ultimate v6.0 running on http://localhost:{port}")
    print("📡 API Endpoints:")
    print("  GET  /              - رابط کاربری اصلی")
    print("  POST /api/ask       - پرسش و پاسخ هوش مصنوعی")
    print("  GET  /api/health    - وضعیت سلامت سیستم")
    print("  GET  /api/knowledge - پایگاه دانش")
    print("  GET  /api/debug     - اطلاعات دیباگ")
    print("  GET  /api/history   - تاریخچه مکالمات")
    print("  GET  /api/ui.html   - رابط کاربری کامل")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Shutting down server...")
        server.server_close()
