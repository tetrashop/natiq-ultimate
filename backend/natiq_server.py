#!/usr/bin/env python3
"""
سرور محلی natiq - پردازش سوالات با منطق پیشرفته
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse

class NatiqHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html = """
            <!DOCTYPE html>
            <html dir="rtl">
            <head>
                <meta charset="utf-8">
                <title>natiq-ultimate</title>
                <style>
                    body { font-family: Tahoma; padding: 20px; }
                    .container { max-width: 600px; margin: auto; }
                    input { width: 100%; padding: 10px; margin: 10px 0; }
                    button { padding: 10px 20px; background: #007bff; color: white; border: none; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🤖 natiq-ultimate</h1>
                    <input id="question" placeholder="سوال خود را بپرسید...">
                    <button onclick="ask()">بپرس</button>
                    <div id="answer"></div>
                </div>
                <script>
                    function ask() {
                        const q = document.getElementById('question').value;
                        fetch('/ask?q=' + encodeURIComponent(q))
                            .then(r => r.json())
                            .then(data => {
                                document.getElementById('answer').innerHTML = 
                                    '<h3>🤖 پاسخ:</h3><p>' + data.answer + '</p>';
                            });
                    }
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
        
        elif self.path.startswith('/ask'):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            question = params.get('q', [''])[0]
            
            # تولید پاسخ
            answer = self.generate_answer(question)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            response = json.dumps({
                "question": question,
                "answer": answer,
                "status": "success"
            }, ensure_ascii=False)
            
            self.wfile.write(response.encode('utf-8'))
    
    def generate_answer(self, question):
        """تولید پاسخ هوشمند"""
        # منطق پاسخ‌دهی
        q_lower = question.lower()
        
        answers = {
            "سلام": "سلام! خوش آمدید. چطور می‌تونم کمک کنم؟",
            "حال": "خوبم ممنون! شما چطورید؟",
            "اسم": "من natiq-ultimate هستم، دستیار هوشمند شما!",
            "ساعت": f"الان ساعت {datetime.now().strftime('%H:%M')} است.",
            "هوش مصنوعی": "هوش مصنوعی علم ساخت ماشین‌های هوشمند است که می‌توانند مانند انسان فکر کنند.",
            "پایتون": "پایتون یک زبان برنامه‌نویسی محبوب برای توسعه وب، علم داده و هوش مصنوعی است."
        }
        
        for key in answers:
            if key in q_lower:
                return answers[key]
        
        return f"سوال جالبی پرسیدید: '{question}'. من در حال یادگیری بیشتر هستم!"

def run_server():
    server = HTTPServer(('localhost', 8080), NatiqHandler)
    print("🌐 سرور natiq در حال اجرا: http://localhost:8080")
    print("📱 در مرورگر خود باز کنید و سوال بپرسید!")
    print("برای توقف: Ctrl+C")
    server.serve_forever()

if __name__ == "__main__":
    from datetime import datetime
    run_server()
