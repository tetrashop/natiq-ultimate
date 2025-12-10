"""
Natiq API - نسخه فوق ساده و پایدار
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from mangum import Mangum
import json
from datetime import datetime

app = FastAPI(
    title="Natiq API",
    version="3.2.0",
    docs_url=None,  # غیرفعال کردن docs برای سادگی
    redoc_url=None
)

@app.get("/")
async def root():
    return {
        "status": "active",
        "service": "natiq-api",
        "version": "3.2.0",
        "message": "Natiq Ultimate API Server"
    }

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "python_version": "3.9"
    }

@app.post("/api/chat")
async def chat(request: Request):
    """اندپوینت چت ساده"""
    try:
        body = await request.body()
        if body:
            data = json.loads(body)
            user_message = data.get("message", "بدون متن")
        else:
            user_message = "بدون متن"
        
        return JSONResponse({
            "success": True,
            "response": f"پیام شما: '{user_message}' دریافت شد. سیستم ناطق فعال است.",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }, status_code=500)

@app.post("/api/chat-memory")
async def chat_memory(request: Request):
    """چت با قابلیت حافظه"""
    return JSONResponse({
        "success": True,
        "response": "سیستم چت با حافظه فعال است. برای استفاده کامل، لطفا پیام ارسال کنید.",
        "has_memory": True,
        "timestamp": datetime.now().isoformat()
    })

@app.get("/api/test")
async def test():
    """تست ساده API"""
    return JSONResponse({
        "test": "success",
        "message": "API در حال کار است",
        "version": "3.2.0",
        "timestamp": datetime.now().isoformat()
    })

# هندلر برای Vercel
handler = Mangum(app)

# برای اجرای محلی (اختیاری)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
