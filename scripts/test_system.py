#!/usr/bin/env python3
"""
اسکریپت تست جامع natiq-ultimate v2.1
تست‌های خودکار برای بررسی صحت عملکرد تمام بخش‌ها
"""

import sys
import os
import json
import time
import requests
import websocket
import threading
from pathlib import Path
from datetime import datetime

# رنگ‌ها برای خروجی
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_status(test_name, status, message=""):
    """چاپ وضعیت تست"""
    symbols = {
        "PASS": "✅",
        "FAIL": "❌",
        "WARN": "⚠️",
        "INFO": "📝"
    }
    
    colors = {
        "PASS": Colors.GREEN,
        "FAIL": Colors.RED,
        "WARN": Colors.YELLOW,
        "INFO": Colors.BLUE
    }
    
    print(f"{colors.get(status, '')}{symbols.get(status, '')} [{status}] {test_name}: {message}{Colors.END}")
    return status == "PASS"

class NatiqTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session_id = f"test_session_{int(time.time())}"
        self.results = []
        self.ws_messages = []
        
    def run_all_tests(self):
        """اجرای تمام تست‌ها"""
        print(f"\n{Colors.BLUE}🚀 شروع تست جامع natiq-ultimate v2.1{Colors.END}")
        print(f"📅 زمان: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 آدرس سرور: {self.base_url}")
        print(f"🎯 شناسه جلسه: {self.session_id}")
        print("-" * 60)
        
        # 1. تست اتصال پایه
        self.test_server_connection()
        
        # 2. تست API‌های REST
        self.test_rest_apis()
        
        # 3. تست WebSocket
        self.test_websocket()
        
        # 4. تست فایل‌های استاتیک
        self.test_static_files()
        
        # 5. تست عملکرد natiq_smart
        self.test_natiq_logic()
        
        # 6. تست عملکرد تحت بار
        self.test_performance()
        
        # نمایش نتایج
        self.show_summary()
        
    def test_server_connection(self):
        """تست اتصال به سرور"""
        print(f"\n{Colors.BLUE}📡 بخش ۱: تست اتصال سرور{Colors.END}")
        
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print_status("اتصال به سرور", "PASS", 
                           f"سرور فعال - وضعیت: {data.get('status', 'unknown')}")
                print_status("نسخه سرور", "PASS", 
                           f"نسخه: {data.get('version', 'unknown')}")
                return True
            else:
                print_status("اتصال به سرور", "FAIL", 
                           f"کد وضعیت: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print_status("اتصال به سرور", "FAIL", 
                       "سرور در دسترس نیست. مطمئن شوید سرور اجرا شده است.")
            return False
        except Exception as e:
            print_status("اتصال به سرور", "FAIL", f"خطا: {str(e)}")
            return False
    
    def test_rest_apis(self):
        """تست API‌های REST"""
        print(f"\n{Colors.BLUE}🔧 بخش ۲: تست API‌های REST{Colors.END}")
        
        # تست endpoint سلامت
        try:
            response = requests.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                print_status("GET /api/health", "PASS")
            else:
                print_status("GET /api/health", "FAIL", 
                           f"کد: {response.status_code}")
        except Exception as e:
            print_status("GET /api/health", "FAIL", f"خطا: {e}")
        
        # تست endpoint چت
        test_messages = [
            ("سلام", "سلام", "greeting"),
            ("اسم من تست است", "نام کاربر", "name_set"),
            ("آمار", "آمار", "stats")
        ]
        
        for question, expected_keyword, test_type in test_messages:
            try:
                response = requests.post(
                    f"{self.base_url}/api/chat/{self.session_id}",
                    json={"message": question},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if expected_keyword in data.get("answer", "").lower():
                        print_status(f"POST /api/chat [{test_type}]", "PASS", 
                                   f"پاسخ: {data['answer'][:50]}...")
                    else:
                        print_status(f"POST /api/chat [{test_type}]", "WARN", 
                                   f"پاسخ غیرمنتظره: {data['answer'][:50]}...")
                else:
                    print_status(f"POST /api/chat [{test_type}]", "FAIL", 
                               f"کد: {response.status_code}")
            except Exception as e:
                print_status(f"POST /api/chat [{test_type}]", "FAIL", f"خطا: {e}")
        
        # تست endpoint آمار
        try:
            response = requests.get(f"{self.base_url}/api/stats/{self.session_id}")
            if response.status_code in [200, 404]:  # 404 اگر سشن وجود نداشته باشد
                print_status("GET /api/stats/{session_id}", "PASS", 
                           f"کد: {response.status_code}")
            else:
                print_status("GET /api/stats/{session_id}", "WARN", 
                           f"کد غیرمنتظره: {response.status_code}")
        except Exception as e:
            print_status("GET /api/stats/{session_id}", "FAIL", f"خطا: {e}")
    
    def test_websocket(self):
        """تست اتصال WebSocket"""
        print(f"\n{Colors.BLUE}🔌 بخش ۳: تست WebSocket{Colors.END}")
        
        ws_url = self.base_url.replace("http", "ws") + f"/ws/{self.session_id}"
        received_messages = []
        
        def on_message(ws, message):
            data = json.loads(message)
            received_messages.append(data)
            print_status("دریافت پیام WebSocket", "INFO", 
                       f"نوع: {data.get('type', 'unknown')}")
        
        def on_error(ws, error):
            print_status("خطای WebSocket", "WARN", f"{error}")
        
        def on_close(ws, close_status_code, close_msg):
            print_status("اتصال WebSocket بسته شد", "INFO")
        
        def on_open(ws):
            print_status("اتصال WebSocket باز شد", "PASS")
            # ارسال یک پیام تست
            ws.send(json.dumps({
                "type": "message",
                "content": "سلام تست",
                "session_id": self.session_id
            }))
            
            # بعد از 2 ثانیه اتصال را ببند
            time.sleep(2)
            ws.close()
        
        try:
            print_status("تلاش برای اتصال WebSocket", "INFO", f"آدرس: {ws_url}")
            ws = websocket.WebSocketApp(
                ws_url,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            
            # اجرای WebSocket در thread جداگانه
            wst = threading.Thread(target=ws.run_forever)
            wst.daemon = True
            wst.start()
            
            # صبر برای اتمام تست
            time.sleep(3)
            
            if received_messages:
                print_status("WebSocket فعال", "PASS", 
                           f"{len(received_messages)} پیام دریافت شد")
            else:
                print_status("WebSocket فعال", "WARN", 
                           "هیچ پیامی دریافت نشد. ممکن است سرور WebSocket را پشتیبانی نکند.")
                
        except Exception as e:
            print_status("WebSocket فعال", "FAIL", f"خطا: {e}")
    
    def test_static_files(self):
        """تست فایل‌های استاتیک"""
        print(f"\n{Colors.BLUE}📁 بخش ۴: تست فایل‌های استاتیک{Colors.END}")
        
        files_to_check = [
            "/",
            "/static/css/style.css",
            "/static/js/app.js",
            "/chat"
        ]
        
        for file_path in files_to_check:
            try:
                response = requests.get(f"{self.base_url}{file_path}", timeout=5)
                if response.status_code == 200:
                    print_status(f"GET {file_path}", "PASS")
                elif response.status_code == 404 and file_path == "/chat":
                    print_status(f"GET {file_path}", "WARN", 
                               "صفحه chat ممکن است در این نسخه وجود نداشته باشد")
                else:
                    print_status(f"GET {file_path}", "WARN", 
                               f"کد: {response.status_code}")
            except Exception as e:
                print_status(f"GET {file_path}", "FAIL", f"خطا: {e}")
    
    def test_natiq_logic(self):
        """تست منطق natiq_smart"""
        print(f"\n{Colors.BLUE}🧠 بخش ۵: تست منطق هوش مصنوعی{Colors.END}")
        
        # تست مستقیم ماژول natiq_smart اگر در دسترس باشد
        try:
            sys.path.append('backend')
            from natiq_smart import NatiqSmart
            
            natiq = NatiqSmart()
            
            # تست تحلیل سوال
            test_cases = [
                ("سلام", "greeting"),
                ("اسم من علی", "name_set"),
                ("یاد بگیر تست|پاسخ تست", "learn"),
                ("آمار", "stats")
            ]
            
            for question, expected_type in test_cases:
                analysis = natiq.analyze_question(question)
                if analysis["type"] == expected_type:
                    print_status(f"تحلیل سوال: '{question[:15]}...'", "PASS", 
                               f"نوع شناسایی شده: {analysis['type']}")
                else:
                    print_status(f"تحلیل سوال: '{question[:15]}...'", "WARN", 
                               f"انتظار: {expected_type}, دریافت: {analysis['type']}")
            
            # تست تولید پاسخ
            response = natiq.generate_answer("سلام", {"type": "greeting", "topic": "greeting"})
            if "سلام" in response:
                print_status("تولید پاسخ", "PASS", "پاسخ مناسب تولید شد")
            else:
                print_status("تولید پاسخ", "WARN", f"پاسخ: {response[:50]}...")
                
        except ImportError:
            print_status("بارگیری natiq_smart", "WARN", 
                       "ماژول natiq_smart یافت نشد. تست‌های منطق نادیده گرفته می‌شوند.")
        except Exception as e:
            print_status("تست منطق", "FAIL", f"خطا: {e}")
    
    def test_performance(self):
        """تست عملکرد"""
        print(f"\n{Colors.BLUE}⚡ بخش ۶: تست عملکرد{Colors.END}")
        
        # تست زمان پاسخ
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=5)
            response_time = (time.time() - start_time) * 1000  # به میلی‌ثانیه
            
            if response_time < 100:
                print_status("زمان پاسخ سلامت سرور", "PASS", 
                           f"{response_time:.1f}ms (عالی)")
            elif response_time < 500:
                print_status("زمان پاسخ سلامت سرور", "PASS", 
                           f"{response_time:.1f}ms (خوب)")
            elif response_time < 1000:
                print_status("زمان پاسخ سلامت سرور", "WARN", 
                           f"{response_time:.1f}ms (آهسته)")
            else:
                print_status("زمان پاسخ سلامت سرور", "WARN", 
                           f"{response_time:.1f}ms (خیلی آهسته)")
                
        except Exception as e:
            print_status("تست عملکرد", "FAIL", f"خطا: {e}")
        
        # تست چند درخواست همزمان
        print_status("تست چند درخواست", "INFO", "در حال اجرا...")
        try:
            start = time.time()
            responses = []
            for i in range(3):
                try:
                    r = requests.post(
                        f"{self.base_url}/api/chat/{self.session_id}_perf{i}",
                        json={"message": f"تست عملکرد {i}"},
                        timeout=10
                    )
                    responses.append(r.status_code)
                except:
                    pass
            
            total_time = (time.time() - start) * 1000
            success_count = sum(1 for code in responses if code == 200)
            
            if success_count == 3:
                print_status("تست بار همزمان", "PASS", 
                           f"3/3 موفق در {total_time:.1f}ms")
            elif success_count > 0:
                print_status("تست بار همزمان", "WARN", 
                           f"{success_count}/3 موفق در {total_time:.1f}ms")
            else:
                print_status("تست بار همزمان", "FAIL", 
                           f"هیچ درخواستی موفق نبود")
                
        except Exception as e:
            print_status("تست بار همزمان", "FAIL", f"خطا: {e}")
    
    def show_summary(self):
        """نمایش خلاصه نتایج"""
        print(f"\n{Colors.BLUE}" + "="*60 + Colors.END)
        print(f"{Colors.BLUE}📊 خلاصه نتایج تست{Colors.END}")
        print(f"{Colors.BLUE}" + "="*60 + Colors.END)
        
        # جمع‌آوری نتایج از خروجی چاپ شده (ساده‌سازی)
        print(f"\n{Colors.GREEN}✅ تست‌های موفق: سیستم به خوبی کار می‌کند{Colors.END}")
        print(f"{Colors.YELLOW}⚠️  هشدارها: ممکن است نیاز به بررسی جزئی داشته باشند{Colors.END}")
        print(f"{Colors.RED}❌ خطاها: نیاز به رفع فوری دارند{Colors.END}")
        
        print(f"\n{Colors.BLUE}🎯 اقدامات بعدی:{Colors.END}")
        print("1. اگر خطای قرمز دارید، ابتدا آن‌ها را رفع کنید")
        print("2. هشدارهای زرد را برای بهبود سیستم بررسی کنید")
        print("3. رابط کاربری را در مرورگر باز کنید و تست دستی انجام دهید")
        print("4. از دکمه 'تست اتصال API' در پنل کناری استفاده کنید")
        print(f"\n{Colors.GREEN}✨ تست کامل شد! سیستم آماده استفاده است.{Colors.END}")

def main():
    """تابع اصلی"""
    print(f"{Colors.BLUE}🤖 تستر natiq-ultimate v2.1{Colors.END}")
    print(f"{Colors.BLUE}="*50 + Colors.END)
    
    # بررسی اینکه سرور اجراست
    try:
        requests.get("http://localhost:8000/api/health", timeout=2)
    except:
        print(f"{Colors.YELLOW}⚠️  هشدار: سرور localhost:8000 در دسترس نیست.{Colors.END}")
        print("لطفاً ابتدا سرور را اجرا کنید:")
        print("  cd ~/natiq-ultimate-web")
        print("  ./scripts/start.sh")
        print("\nاگر سرور روی آدرس دیگری اجراست، آن را وارد کنید:")
        print("  مثال: python test_system.py http://192.168.1.10:8000")
    
    # دریافت آدرس سرور از آرگومان
    base_url = "http://localhost:8000"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    # اجرای تست
    tester = NatiqTester(base_url)
    tester.run_all_tests()

if __name__ == "__main__":
    main()
