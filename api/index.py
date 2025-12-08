from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json
import os

app = FastAPI(title="natiq-ultimate API", version="6.0")

# فعال کردن CORS - بسیار مهم برای Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # در تولید بهتر است دامنه خاصی بگذارید
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# مدل داده برای درخواست سوال
class QuestionRequest(BaseModel):
    question: str
    session_id: Optional[str] = None

# ============ ENDPOINTها ============

@app.get("/api/health")
async def health_check():
    """بررسی سلامت سیستم"""
    return {
        "status": "healthy",
        "version": "6.0",
        "service": "natiq-ultimate",
        "environment": os.environ.get("VERCEL_ENV", "production")
    }

@app.get("/api/knowledge")
async def get_knowledge():
    """لیست دانش پایه"""
    return {
        "success": True,
        "count": 5,
        "knowledge": [
            {"id": 1, "question": "هوش مصنوعی چیست؟", "answer": "شاخه‌ای از علوم کامپیوتر برای ساخت ماشین‌های هوشمند"},
            {"id": 2, "question": "NLP چیست؟", "answer": "پردازش زبان طبیعی برای تعامل کامپیوتر با زبان انسان"}
        ]
    }

@app.post("/api/ask")
async def ask_question(request: QuestionRequest):
    """دریافت پاسخ برای سوال - SIMPLE VERSION"""
    try:
        question = request.question.lower().strip()
        
        # پایگاه دانش ساده
        responses = {
            "سلام": "سلام! به natiq-ultimate خوش آمدید. چطور می‌توانم کمک کنم؟",
            "هوش مصنوعی": "هوش مصنوعی (AI) شاخه‌ای از علوم کامپیوتر است که به ساخت ماشین‌های هوشمند می‌پردازد.",
            "nlp": "پردازش زبان طبیعی (NLP) شاخه‌ای از هوش مصنوعی برای تعامل با زبان انسان است.",
            "یادگیری ماشین": "یادگیری ماشین (ML) زیرشاخه‌ای از AI که به سیستم‌ها توانایی یادگیری خودکار می‌دهد.",
            "شبکه عصبی": "شبکه عصبی مصنوعی از نورون‌های مصنوعی برای پردازش اطلاعات استفاده می‌کند.",
            "چطوری": "خوبم ممنون! شما چطورید؟",
            "اسمت چیه": "من natiq-ultimate هستم، یک سیستم عصبی-نمادین هوشمند.",
            "چکار میتونی بکنی": "می‌توانم به سوالات شما درباره هوش مصنوعی، یادگیری ماشین، NLP و موضوعات مرتبط پاسخ دهم."
        }
        
        # پیدا کردن پاسخ مناسب
        answer = None
        for key in responses:
            if key in question:
                answer = responses[key]
                break
        
        if not answer:
            answer = f"""شما پرسیدید: "{request.question}"

من natiq-ultimate هستم، یک سیستم عصبی-نمادین.
می‌توانم در مورد این موضوعات کمک کنم:
• هوش مصنوعی و یادگیری ماشین
• پردازش زبان طبیعی (NLP)
• شبکه‌های عصبی
• سیستم‌های مبتنی بر دانش

لطفاً سوال خود را با جزئیات بیشتری بپرسید."""

        return {
            "success": True,
            "response": answer,
            "question": request.question,
            "session_id": request.session_id or "vercel-session"
        }
        
    except Exception as e:
        return {
            "success": False,
            "response": "متأسفانه در پردازش سوال شما مشکلی رخ داد.",
            "error": str(e),
            "question": request.question if 'request' in locals() else "unknown"
        }

@app.get("/api/debug")
async def debug_info():
    """اطلاعات دیباگ"""
    import platform
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "env": dict(os.environ)
    }

# برای تست محلی
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
