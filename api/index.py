from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI(title="natiq-ultimate API", version="6.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "natiq-ultimate API is running"}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "6.0",
        "service": "natiq-ultimate",
        "environment": "production"
    }

@app.post("/api/ask")
async def ask_question(request: dict):  # استفاده از dict به جای Pydantic model
    """
    دریافت سوال و پاسخ دادن
    """
    try:
        print(f"📥 درخواست دریافت شد: {request}")
        
        # استخراج سوال
        question = request.get("question", "").strip()
        session_id = request.get("session_id", "default-session")
        
        if not question:
            return {
                "success": False,
                "response": "لطفاً یک سوال وارد کنید.",
                "error": "Empty question"
            }
        
        # پایگاه دانش ساده
        knowledge = {
            "سلام": "سلام! به natiq-ultimate خوش آمدید. چطور می‌توانم کمک کنم؟",
            "هوش مصنوعی": "هوش مصنوعی (AI) شاخه‌ای از علوم کامپیوتر است که به ساخت ماشین‌های هوشمند می‌پردازد.",
            "nlp": "پردازش زبان طبیعی (NLP) شاخه‌ای از هوش مصنوعی برای تعامل با زبان انسان است.",
            "یادگیری ماشین": "یادگیری ماشین (ML) زیرشاخه‌ای از AI که به سیستم‌ها توانایی یادگیری خودکار می‌دهد.",
            "چطوری": "خوبم ممنون! شما چطورید؟",
            "اسمت چیه": "من natiq-ultimate هستم، یک سیستم عصبی-نمادین هوشمند.",
            "test": "This is a test response from Vercel API.",
            "تست": "این یک پاسخ تست از API ورسل است."
        }
        
        # جستجوی پاسخ
        answer = None
        question_lower = question.lower()
        
        for key in knowledge:
            if key.lower() in question_lower:
                answer = knowledge[key]
                break
        
        # اگر پاسخ پیدا نشد
        if not answer:
            answer = f"""شما پرسیدید: "{question}"

من natiq-ultimate هستم، یک سیستم عصبی-نمادین.
می‌توانم در مورد موضوعات زیر کمک کنم:
• هوش مصنوعی و یادگیری ماشین
• پردازش زبان طبیعی (NLP)
• شبکه‌های عصبی
• سیستم‌های مبتنی بر دانش

لطفاً سوال خود را با جزئیات بیشتری بپرسید."""
        
        print(f"📤 پاسخ ارسال می‌شود: {answer[:50]}...")
        
        return {
            "success": True,
            "response": answer,
            "question": question,
            "session_id": session_id,
            "source": "vercel-api"
        }
        
    except Exception as e:
        print(f"❌ خطا در /api/ask: {str(e)}")
        return {
            "success": False,
            "response": "متأسفانه در پردازش سوال شما مشکلی رخ داد.",
            "error": str(e),
            "question": question if 'question' in locals() else "unknown"
        }

@app.get("/api/knowledge")
async def get_knowledge():
    return {
        "success": True,
        "count": 2,
        "knowledge": [
            {"id": 1, "topic": "AI", "description": "هوش مصنوعی"},
            {"id": 2, "topic": "NLP", "description": "پردازش زبان طبیعی"}
        ]
    }

@app.get("/api/test")
async def test_endpoint():
    """Endpoint تست ساده"""
    return {"message": "Test successful", "status": "working"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
