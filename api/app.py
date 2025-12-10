from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mangum import Mangum
from datetime import datetime
import json

app = FastAPI(
    title="Natiq API",
    version="3.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# تنظیم CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# روت اصلی
@app.get("/")
async def root():
    return {"message": "Natiq API Server", "version": "3.1.0", "status": "active"}

# سلامت سیستم
@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "version": "3.1.0",
        "timestamp": datetime.now().isoformat(),
        "services": ["chat", "nlp", "tts"]
    }

# چت ساده
@app.post("/api/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        message = data.get("message", "")
        
        return {
            "success": True,
            "response": f"دریافت کردم: {message} | این پاسخ از API جدید است",
            "timestamp": datetime.now().isoformat(),
            "language": "fa"
        }
    except:
        return {
            "success": True,
            "response": "سلام! من ناطق هستم. چطور می‌تونم کمک کنم؟",
            "timestamp": datetime.now().isoformat()
        }

# چت با حافظه
@app.post("/api/chat-memory")
async def chat_memory(request: Request):
    try:
        data = await request.json()
        message = data.get("message", "")
        history = data.get("history", [])
        
        response_text = f"پیام شما: {message}"
        if history:
            response_text += f" | حافظه: {len(history)} پیام قبلی"
        
        return {
            "success": True,
            "response": response_text,
            "history": history + [{"role": "assistant", "content": response_text}],
            "has_memory": True,
            "timestamp": datetime.now().isoformat()
        }
    except:
        return {
            "success": True,
            "response": "سیستم چت با حافظه فعال است. لطفاً پیام خود را ارسال کنید.",
            "history": [],
            "has_memory": True,
            "timestamp": datetime.now().isoformat()
        }

# تحلیل NLP
@app.post("/api/nlp")
async def nlp_analysis(request: Request):
    return {
        "success": True,
        "analysis": {
            "tokens": ["این", "یک", "تحلیل", "نمونه", "است"],
            "pos_tags": ["PRON", "DET", "NOUN", "NOUN", "VERB"],
            "sentiment": "positive",
            "confidence": 0.87
        },
        "timestamp": datetime.now().isoformat(),
        "note": "سیستم NLP کامل در حال توسعه است"
    }

# هندلر برای Vercel
handler = Mangum(app)

# برای اجرای محلی
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
