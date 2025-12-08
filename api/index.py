from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "healthy", "version": "6.0", "environment": "vercel"}

@app.get("/api/debug")
def debug_info():
    import sys
    return {
        "python": sys.version.split()[0],
        "endpoints": ["/api/health", "/api/ask", "/api/knowledge", "/api/debug"]
    }

@app.post("/api/ask")
def ask_question(question: dict):
    """نسخه ساده و کارآمد - شبیه ask-simple"""
    try:
        q = question.get("question", "").strip()
        session = question.get("session_id", "default")
        
        if not q:
            return {
                "success": False,
                "response": "لطفاً یک سوال وارد کنید."
            }
        
        # پایگاه دانش
        answers = {
            "سلام": "سلام! به natiq-ultimate روی Vercel خوش آمدید!",
            "هوش مصنوعی": "هوش مصنوعی (AI) شاخه‌ای از علوم کامپیوتر است.",
            "nlp": "پردازش زبان طبیعی (NLP) برای تعامل با زبان انسان است.",
            "test": "Test successful from Vercel API!",
            "تست": "تست موفق از API ورسل!"
        }
        
        # جستجو
        response_text = answers.get(q.lower(), "")
        if not response_text:
            for key in answers:
                if key in q.lower():
                    response_text = answers[key]
                    break
        
        if not response_text:
            response_text = f"""شما پرسیدید: "{q}"

natiq-ultimate v6.0 روی Vercel در حال اجراست.
می‌توانم در مورد موضوعات زیر کمک کنم:
• هوش مصنوعی و یادگیری ماشین
• پردازش زبان طبیعی
• شبکه‌های عصبی

سوال خود را با جزئیات بیشتری بپرسید."""
        
        return {
            "success": True,
            "response": response_text,
            "question": q,
            "session_id": session,
            "source": "vercel-production"
        }
        
    except Exception as e:
        return {
            "success": False,
            "response": "خطا در پردازش",
            "error": str(e)[:100]
        }

@app.get("/api/knowledge")
def get_knowledge():
    return {
        "success": True,
        "count": 3,
        "knowledge": [
            {"id": 1, "topic": "AI", "desc": "هوش مصنوعی"},
            {"id": 2, "topic": "NLP", "desc": "پردازش زبان طبیعی"},
            {"id": 3, "topic": "ML", "desc": "یادگیری ماشین"}
        ]
    }

@app.get("/")
def root():
    return {"message": "natiq-ultimate API", "status": "operational"}
