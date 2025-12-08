from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()

# فعال‌سازی کامل CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # اجازه همه origins
    allow_credentials=True,
    allow_methods=["*"],  # اجازه همه متدها
    allow_headers=["*"],  # اجازه همه هدرها
)

class QuestionRequest(BaseModel):
    question: str
    session_id: Optional[str] = None

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "version": "6.0",
        "knowledge_count": 15,
        "timestamp": "2024-12-08",
        "message": "natiq-ultimate v6.0 - سیستم عصبی نمادین"
    }

@app.get("/api/knowledge")
async def knowledge():
    return {
        "success": True,
        "count": 15,
        "knowledge": [
            {"id": 1, "question": "AI چیست؟", "answer": "هوش مصنوعی"},
            {"id": 2, "question": "NLP چیست؟", "answer": "پردازش زبان طبیعی"}
        ]
    }

@app.post("/api/ask")
async def ask_question(request: QuestionRequest):
    """دریافت پاسخ برای سوال"""
    try:
        question = request.question.lower()
        
        # پایگاه دانش ساده
        knowledge_base = {
            "سلام": "سلام! به natiq-ultimate خوش آمدید. چطور می‌توانم کمک کنم؟",
            "هوش مصنوعی": "هوش مصنوعی (AI) شاخه‌ای از علوم کامپیوتر است که به ساخت ماشین‌های هوشمند می‌پردازد.",
            "nlp": "پردازش زبان طبیعی (NLP) شاخه‌ای از هوش مصنوعی است که به تعامل بین کامپیوتر و زبان انسان می‌پردازد.",
            "یادگیری ماشین": "یادگیری ماشین (ML) زیرشاخه‌ای از هوش مصنوعی است که به سیستم‌ها توانایی یادگیری خودکار می‌دهد.",
            "شبکه عصبی": "شبکه عصبی مصنوعی از نورون‌های مصنوعی برای پردازش اطلاعات استفاده می‌کند.",
            "natiq": "natiq-ultimate یک سیستم عصبی-نمادین است که ترکیبی از شبکه عصبی و منطق نمادین است.",
            "رابط کاربری": "این رابط کاربری با HTML/CSS/JavaScript ساخته شده و با FastAPI ارتباط برقرار می‌کند."
        }
        
        # پیدا کردن پاسخ مناسب
        response_text = "شما پرسیدید: '" + request.question + "'\n\n"
        found = False
        
        for key, value in knowledge_base.items():
            if key in question:
                response_text = value
                found = True
                break
        
        if not found:
            response_text += """من natiq-ultimate هستم، یک سیستم عصبی-نمادین هوشمند.

من می‌توانم در مورد موضوعات زیر اطلاعات ارائه دهم:
• هوش مصنوعی و یادگیری ماشین
• پردازش زبان طبیعی (NLP)
• شبکه‌های عصبی
• سیستم‌های مبتنی بر دانش
• برنامه‌نویسی و فناوری

لطفاً سوال خود را با جزئیات بیشتری بپرسید."""

        return {
            "success": True,
            "response": response_text,
            "question": request.question,
            "session_id": request.session_id or "session_" + str(hash(request.question))
        }
        
    except Exception as e:
        return {
            "success": False,
            "response": "متأسفانه خطایی در پردازش سوال شما رخ داد.",
            "error": str(e)
        }

@app.get("/")
async def root():
    return {"message": "API Server is running"}

if __name__ == "__main__":
    print("🚀 API سرور روی پورت 8081 راه‌اندازی شد")
    uvicorn.run(app, host="127.0.0.1", port=8081, log_level="info")
