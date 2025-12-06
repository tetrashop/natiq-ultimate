#!/usr/bin/env python3
"""
مانیتور آپ‌تایم API
"""

import requests
import time
import json
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from typing import Dict, List

class UptimeMonitor:
    def __init__(self, api_url: str, check_interval: int = 300):
        self.api_url = api_url
        self.check_interval = check_interval
        self.uptime_data = []
        self.downtime_events = []
        
    def check_status(self) -> Dict:
        """بررسی وضعیت فعلی API"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.api_url}/api/health", timeout=30)
            response_time = time.time() - start_time
            
            return {
                "timestamp": datetime.now().isoformat(),
                "status_code": response.status_code,
                "response_time": response_time,
                "success": response.status_code == 200
            }
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "success": False
            }
    
    def calculate_uptime(self, hours: int = 24) -> float:
        """محاسبه آپ‌تایم در N ساعت گذشته"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        relevant_data = [d for d in self.uptime_data 
                        if datetime.fromisoformat(d["timestamp"]) > cutoff_time]
        
        if not relevant_data:
            return 0.0
        
        successful = sum(1 for d in relevant_data if d.get("success", False))
        return (successful / len(relevant_data)) * 100
    
    def run(self):
        """اجرای مانیتور"""
        print(f"🚀 شروع مانیتورینگ: {self.api_url}")
        print(f"📊 بازه بررسی: هر {self.check_interval} ثانیه")
        print("-" * 60)
        
        try:
            while True:
                result = self.check_status()
                self.uptime_data.append(result)
                
                # نگه داشتن فقط 1000 رکورد آخر
                if len(self.uptime_data) > 1000:
                    self.uptime_data = self.uptime_data[-1000:]
                
                # نمایش وضعیت
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if result["success"]:
                    print(f"[{timestamp}] ✅ سالم | زمان: {result.get('response_time', 0):.2f}s")
                else:
                    error_msg = result.get('error', f"کد وضعیت: {result.get('status_code')}")
                    print(f"[{timestamp}] ❌ خطا | {error_msg}")
                    
                    # ثبت downtime
                    self.downtime_events.append({
                        "start": result["timestamp"],
                        "error": error_msg
                    })
                
                # گزارش ساعتی
                if datetime.now().minute == 0:
                    uptime_24h = self.calculate_uptime(24)
                    uptime_1h = self.calculate_uptime(1)
                    print(f"📈 آپ‌تایم: 1h={uptime_1h:.1f}% | 24h={uptime_24h:.1f}%")
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            print("\n⏹️  توقف مانیتورینگ")
            
            # خلاصه نهایی
            if self.uptime_data:
                total = len(self.uptime_data)
                successful = sum(1 for d in self.uptime_data if d["success"])
                uptime = (successful / total) * 100
                print(f"\n📊 خلاصه نهایی:")
                print(f"   کل بررسی‌ها: {total}")
                print(f"   موفق: {successful}")
                print(f"   آپ‌تایم: {uptime:.2f}%")
                print(f"   Downtime Events: {len(self.downtime_events)}")

if __name__ == "__main__":
    # تنظیمات
    API_URL = "https://natiq-ultimate.vercel.app"  # تغییر به آدرس واقعی
    CHECK_INTERVAL = 300  # ثانیه
    
    monitor = UptimeMonitor(API_URL, CHECK_INTERVAL)
    monitor.run()
