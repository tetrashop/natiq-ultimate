#!/usr/bin/env python3
"""
تست عملکرد پایه NLP
"""

import sys
from pathlib import Path

# اضافه کردن مسیر src به sys.path
sys.path.append(str(Path(__file__).parent))

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
    import torch
    print("✅ کتابخانه‌ها بارگذاری شدند")
except ImportError as e:
    print(f"❌ خطا در واردسازی کتابخانه‌ها: {e}")
    print("لطفا دستور زیر را اجرا کنید:")
    print("pip install transformers torch")
    sys.exit(1)

def test_simple_chat():
    """تست ساده گفتگو"""
    print("\n🧪 تست سیستم پرسش و پاسخ")
    print("-" * 40)
    
    # استفاده از یک مدل کوچک و سریع
    model_name = "google/flan-t5-small"  # مدل سبک و سریع
    
    print(f"📥 در حال بارگذاری مدل: {model_name}")
    print("لطفا منتظر بمانید (ممکن است چند دقیقه طول بکشد)...")
    
    try:
        # ساخت pipeline برای متن به متن
        qa_pipeline = pipeline(
            "text2text-generation",
            model=model_name,
            device=-1  # استفاده از CPU
        )
        
        print("✅ مدل بارگذاری شد!")
        
        while True:
            print("\n" + "=" * 50)
            question = input("سوال خود را بپرسید (یا 'خروج' برای پایان): ")
            
            if question.lower() in ['خروج', 'exit', 'quit']:
                print("👋 خداحافظ!")
                break
            
            if not question.strip():
                print("⚠️ لطفا یک سوال وارد کنید")
                continue
            
            print(f"\n📝 شما پرسیدید: {question}")
            print("🤔 در حال پردازش...")
            
            try:
                # تولید پاسخ
                result = qa_pipeline(
                    question,
                    max_length=100,
                    do_sample=True,
                    temperature=0.7
                )
                
                answer = result[0]['generated_text']
                print(f"🤖 پاسخ: {answer}")
                
            except Exception as e:
                print(f"❌ خطا در پردازش: {e}")
                print("شاید مدل در حال دانلود است...")
        
    except Exception as e:
        print(f"❌ خطا در بارگذاری مدل: {e}")
        print("\nراه‌حل‌های ممکن:")
        print("1. اطمینان از اتصال به اینترنت")
        print("2. نصب مجدد transformers: pip install --upgrade transformers")
        print("3. استفاده از مدل کوچکتر")

if __name__ == "__main__":
    print("🚀 شروع تست natiq-ultimate")
    test_simple_chat()
