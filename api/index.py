from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import json
import os
import sys

# اضافه کردن مسیر پروژه به sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="natiq-ultimate API", version="6.0")

# فعال کردن CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# سرو فایل‌های استاتیک از پوشه public
app.mount("/", StaticFiles(directory="../public", html=True), name="static")

# مدل‌های داده
class QuestionRequest(BaseModel):
    question: str
    session_id: Optional[str] = None

class QuestionResponse(BaseModel):
    success: bool
    response: str
    error: Optional[str] = None

# تابع برای بارگذاری دانش
def load_knowledge_base():
    try:
        knowledge_file = 'data/knowledge_base.json'
        if os.path.exists(knowledge_file):
            with open(knowledge_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # ایجاد فایل دانش پایه
            base_knowledge = [
                {
                    "id": 1,
                    "question": "هوش مصنوعی چیست؟",
                    "answer": "هوش مصنوعی (AI) شاخه‌ای از علوم کامپیوتر است که به ساخت ماشین‌های هوشمند می‌پردازد.",
                    "category": "مفاهیم پایه"
                }
            ]
            os.makedirs('data', exist_ok=True)
            with open(knowledge_file, 'w', encoding='utf-8') as f:
                json.dump(base_knowledge, f, ensure_ascii=False, indent=2)
            return base_knowledge
    except Exception as e:
        print(f"خطا در بارگذاری دانش: {e}")
        return []

# ==================== ENDPOINTهای API ====================

@app.get("/api/health")
async def health_check():
    """بررسی سلامت سیستم"""
    try:
        knowledge = load_knowledge_base()
        return {
            "status": "healthy",
            "version": "6.0",
            "knowledge_count": len(knowledge),
            "timestamp": "2024-12-08T10:00:00Z"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "2024-12-08T10:00:00Z"
        }

@app.get("/api/knowledge")
async def get_knowledge():
    """دریافت تمام دانش پایه"""
    try:
        knowledge = load_knowledge_base()
        return {
            "success": True,
            "count": len(knowledge),
            "knowledge": knowledge
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/api/ask")
async def ask_question(request: QuestionRequest):
    """دریافت پاسخ برای سوال"""
    try:
        question = request.question
        return {
            "success": True,
            "response": f"شما پرسیدید: {question}\nاین یک پاسخ نمونه از natiq-ultimate v6.0 است.",
            "question": question
        }
    except Exception as e:
        return {
            "success": False,
            "response": "",
            "error": str(e)
        }

@app.get("/api/debug")
async def debug_info():
    """اطلاعات دیباگ سیستم"""
    import platform
    import datetime
    return {
        "system": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "current_time": datetime.datetime.now().isoformat()
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
