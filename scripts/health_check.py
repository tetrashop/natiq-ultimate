#!/usr/bin/env python3
"""
اسکریپت بررسی سلامت API
"""

import requests
import time
import json
import sys
from datetime import datetime

def check_api_health(api_url):
    """بررسی سلامت API"""
    try:
        start_time = time.time()
        response = requests.get(f"{api_url}/api/health", timeout=10)
        response_time = (time.time() - start_time) * 1000  # میلی‌ثانیه
        
        if response.status_code == 200:
            data = response.json()
            return {
                "status": "healthy",
                "response_time": round(response_time, 2),
                "details": data,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "unhealthy",
                "status_code": response.status_code,
                "response_time": round(response_time, 2),
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def main():
    # URL API (می‌تواند از آرگومان گرفته شود)
    api_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
    
    print(f"🔍 بررسی سلامت API: {api_url}")
    print("-" * 50)
    
    # انجام 3 تست متوالی
    results = []
    for i in range(3):
        print(f"تست {i+1}...")
        result = check_api_health(api_url)
        results.append(result)
        
        if result["status"] == "healthy":
            print(f"  ✅ سالم | زمان پاسخ: {result['response_time']}ms")
            if "details" in result:
                print(f"     مدل: {result['details'].get('model_loaded', False)}")
                print(f"     محیط: {result['details'].get('environment', 'N/A')}")
        else:
            print(f"  ❌ مشکل: {result.get('error', result.get('status_code', 'N/A'))}")
        
        if i < 2:
            time.sleep(1)  # وقفه بین تست‌ها
    
    # خلاصه نتایج
    print("-" * 50)
    successful = sum(1 for r in results if r["status"] == "healthy")
    
    if successful == 3:
        print("🎉 API کاملاً سالم است")
        sys.exit(0)
    elif successful >= 1:
        print("⚠️  API نیمه‌سالم است")
        sys.exit(1)
    else:
        print("🔴 API پایین است")
        sys.exit(2)

if __name__ == "__main__":
    main()
