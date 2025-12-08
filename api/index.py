from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import traceback

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
    return {"status": "healthy", "version": "6.0"}

@app.get("/api/test")
def test():
    return {"message": "GET test works"}

@app.post("/api/ask")
async def ask_question(request: Request):
    """ساده‌ترین نسخه - فقط برای دیباگ"""
    try:
        # لاگ شروع
        print("🔍 /api/ask endpoint called")
        
        # خواندن body
        body = await request.body()
        print(f"📥 Raw body: {body}")
        
        # پارس کردن JSON
        data = await request.json()
        print(f"📝 Parsed JSON: {data}")
        
        # پاسخ ساده
        response = {
            "success": True,
            "response": f"شما پرسیدید: '{data.get('question', '')}'. تست Vercel موفق!",
            "debug": "Endpoint /api/ask is working"
        }
        
        print(f"📤 Response: {response}")
        return response
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {str(e)}")
        return {
            "success": False,
            "error": "Invalid JSON format",
            "details": str(e)
        }
    except Exception as e:
        print(f"❌ General error: {str(e)}")
        print(f"🔍 Traceback: {traceback.format_exc()}")
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@app.post("/api/ask-simple")
def ask_simple(question: dict):
    """حتی ساده‌تر - بدون async"""
    return {
        "success": True,
        "response": f"Simple endpoint: {question.get('question', 'no question')}",
        "note": "This is the simple endpoint"
    }

@app.get("/api/debug")
def debug_info():
    """اطلاعات دیباگ"""
    import sys
    return {
        "python_version": sys.version,
        "platform": sys.platform,
        "modules": list(sys.modules.keys())[:20]
    }
