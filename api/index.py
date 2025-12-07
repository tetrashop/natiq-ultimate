"""
natiq-ultimate - Vercel-Compatible API Endpoint
Simple handler for Vercel Serverless Functions.
"""
import json
from http.server import BaseHTTPRequestHandler
import sys

# ✅ AI System Logic (Keep this part from your original code)
class NatiqAISystem:
    def __init__(self):
        self.knowledge_base = {
            "هوش مصنوعی": "شاخه‌ای از علوم کامپیوتر که به ساخت ماشین‌های هوشمند می‌پردازد.",
            "یادگیری ماشین": "توانایی سیستم‌ها برای یادگیری از داده بدون برنامه‌نویسی صریح.",
        }
        self.history = []

    def process_question(self, question):
        """Core AI processing - simplified for example"""
        answer = self.knowledge_base.get(
            question, 
            "متاسفانه پاسخ این سوال را نمی‌دانم. در حال یادگیری هستم!"
        )
        self.history.append({"question": question, "answer": answer[:50]})
        return answer

# ✅ Initialize AI system
ai_system = NatiqAISystem()

# ✅ Vercel-Compatible Handler Class
class Handler(BaseHTTPRequestHandler):
    """Required class for Vercel. DO NOT instantiate this manually."""

    def do_GET(self):
        """Handle GET requests (e.g., for health check)."""
        if self.path == '/health':
            self.send_success({'status': 'System is operational'})
        else:
            # Serve a simple HTML page for the root path
            html = self._generate_html_interface()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        """Handle POST requests (e.g., for asking questions)."""
        if self.path == '/api/ask':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                question = data.get('question', '').strip()
                
                if not question:
                    self.send_error(400, 'سوال نمی‌تواند خالی باشد')
                    return
                
                # Process the question
                answer = ai_system.process_question(question)
                self.send_success({
                    'question': question,
                    'answer': answer,
                    'history_count': len(ai_system.history)
                })
                
            except json.JSONDecodeError:
                self.send_error(400, 'فرمت JSON نامعتبر است')
            except Exception as e:
                self.send_error(500, f'خطای سرور: {str(e)}')
        else:
            self.send_error(404, 'مسیر یافت نشد')

    def send_success(self, data):
        """Helper to send a successful JSON response."""
        response = json.dumps({'success': True, **data}, ensure_ascii=False)
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

    def send_error(self, code, message):
        """Helper to send an error response."""
        response = json.dumps({'success': False, 'error': message}, ensure_ascii=False)
        self.send_response(code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

    def _generate_html_interface(self):
        """Generate a simple HTML interface."""
        return """
        <!DOCTYPE html>
        <html dir="rtl" lang="fa">
        <head><meta charset="UTF-8"><title>natiq-ultimate</title></head>
        <body>
            <h1>🧠 natiq-ultimate v6.0</h1>
            <p>سیستم عصبی-نمادین فعال است. از API endpoint /api/ask استفاده کنید.</p>
        </body>
        </html>
        """

    # ✅ Suppress default log output
    def log_message(self, format, *args):
        pass

# ✅ Vercel's REQUIRED entry point
# Vercel will look for this variable and use the Handler class
handler = Handler

# If run locally for testing
if __name__ == "__main__":
    from http.server import HTTPServer
    print("Running locally on http://localhost:3000")
    server = HTTPServer(('localhost', 3000), Handler)
    server.serve_forever()
