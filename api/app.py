#!/usr/bin/env python3
"""
فایل اصلی FastAPI برای پروژه natiq-ultimate
با قابلیت اتصال به OpenAI API
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import logging
import os
import json
import asyncio
from typing import Optional

# تنظیمات لاگ‌گیری
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# تنظیم OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.warning("⚠️ OPENAI_API_KEY یافت نشد! از مدل محلی استفاده می‌شود.")
    client = None
else:
    client = OpenAI(api_key=OPENAI_API_KEY)
    logger.info("✅ OpenAI API پیکربندی شد")

# ایجاد نمونه FastAPI
app = FastAPI(
    title="Natiq Ultimate AI",
    description="هوش مصنوعی فارسی با قابلیت پردازش متن",
    version="1.5.0",
    docs_url=None,
    redoc_url=None,
    openapi_url="/api/openapi.json"
)

# تنظیم CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# سیستم حافظه مکالمه
conversation_memory = {}

def get_or_create_memory(session_id: str):
    """ایجاد یا بازیابی حافظه مکالمه"""
    if session_id not in conversation_memory:
        conversation_memory[session_id] = {
            "history": [],
            "context": "شما یک دستیار هوش مصنوعی فارسی به نام 'ناطق اولتیمیت' هستید. شما مهربان، مفید و دقیق هستید. به سوالات به زبان فارسی پاسخ می‌دهید.",
            "created_at": asyncio.get_event_loop().time()
        }
    return conversation_memory[session_id]

def cleanup_old_memory(max_age_hours=24):
    """پاکسازی حافظه قدیمی"""
    current_time = asyncio.get_event_loop().time()
    to_delete = []
    
    for session_id, memory in conversation_memory.items():
        age_hours = (current_time - memory["created_at"]) / 3600
        if age_hours > max_age_hours:
            to_delete.append(session_id)
    
    for session_id in to_delete:
        del conversation_memory[session_id]
    if to_delete:
        logger.info(f"🧹 {len(to_delete)} مکالمه قدیمی پاکسازی شد")

async def call_openai(prompt: str, session_id: str = "default") -> str:
    """فراخوانی OpenAI API"""
    
    # اگر API Key نبود، از مدل محلی استفاده کن
    if not client:
        return await get_fallback_response(prompt, session_id)
    
    memory = get_or_create_memory(session_id)
    
    # ساخت تاریخچه مکالمه
    messages = [
        {"role": "system", "content": memory["context"]},
    ]
    
    # اضافه کردن تاریخچه مکالمه (آخرین ۱۰ پیام)
    for msg in memory["history"][-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    
    messages.append({"role": "user", "content": prompt})
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            stream=False
        )
        
        ai_response = response.choices[0].message.content
        
        # ذخیره در حافظه
        memory["history"].append({"role": "user", "content": prompt})
        memory["history"].append({"role": "assistant", "content": ai_response})
        
        # محدود کردن اندازه تاریخچه
        if len(memory["history"]) > 20:
            memory["history"] = memory["history"][-20:]
        
        return ai_response
        
    except Exception as e:
        logger.error(f"❌ خطا در OpenAI API: {str(e)}")
        return await get_fallback_response(prompt, session_id)

async def get_fallback_response(prompt: str, session_id: str) -> str:
    """پاسخ جایگزین در صورت عدم اتصال به OpenAI"""
    
    memory = get_or_create_memory(session_id)
    
    # آنالیز سوال
    prompt_lower = prompt.lower()
    
    # پاسخ‌های هوشمند جایگزین
    responses = {
        "سلام": "سلام! 👋 به ناطق اولتیمیت خوش آمدید. چطور می‌توانم کمکتان کنم؟",
        "خداحافظ": "خداحافظ! 👋 از صحبت با شما خوشحال شدم. اگر سوال دیگری دارید در خدمتم.",
        "چطوری": "من خوبم ممنون! 😊 شما چطورید؟",
        "اسمت چیه": "من ناطق اولتیمیت هستم، یک دستیار هوش مصنوعی فارسی.",
        "کمک": "حتماً! در چه زمینه‌ای می‌تونم کمک کنم؟",
        "هوش مصنوعی": "هوش مصنوعی شاخه‌ای از علوم کامپیوتر است که به ایجاد ماشین‌هایی می‌پردازد که می‌توانند مانند انسان فکر کنند و یاد بگیرند.",
        "openai": "بله، من از OpenAI استفاده می‌کنم. اگر API Key تنظیم شده باشد، می‌توانم از مدل‌های پیشرفته GPT استفاده کنم.",
        "تشکر": "خواهش می‌کنم! 😊 همیشه در خدمت شما هستم.",
        "زمان": f"زمان سرور: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    }
    
    # جستجوی پاسخ مناسب
    for keyword, response in responses.items():
        if keyword in prompt_lower:
            return response
    
    # اگر سوال تکراری است
    if len(memory["history"]) > 0:
        last_q = memory["history"][-1]["content"].lower() if memory["history"][-1]["role"] == "user" else ""
        if prompt_lower == last_q:
            return "به نظر می‌رسد همین سوال را پرسیده‌اید! آیا پاسخ من کافی نبود؟"
    
    # پاسخ پیش‌فرض هوشمند
    if "چی" in prompt_lower and "؟" in prompt:
        return f"شما پرسیدید: '{prompt}'. من یک دستیار هوش مصنوعی هستم و سعی می‌کنم بهترین پاسخ را بدهم!"
    
    return "متوجه سوال شما شدم! در حال حاضر اتصال به OpenAI برقرار نیست. برای پاسخ‌های پیشرفته‌تر لطفاً API Key را تنظیم کنید."

# ==================== مسیرهای API ====================

@app.get("/")
async def root():
    """صفحه اصلی"""
    return FileResponse("public/index.html")

@app.get("/api/")
async def api_root():
    """اطلاعات API"""
    has_openai = bool(client)
    return {
        "message": "به ناطق اولتیمیت خوش آمدید",
        "status": "active",
        "version": "1.5.0",
        "ai_capabilities": {
            "openai_connected": has_openai,
            "memory_enabled": True,
            "persian_support": True,
            "fallback_mode": not has_openai
        },
        "endpoints": {
            "chat": "/api/chat",
            "health": "/api/health",
            "status": "/api/status",
            "clear_memory": "/api/clear-memory",
            "docs": "/api/docs"
        }
    }

@app.get("/api/health")
async def health_check():
    """بررسی سلامت"""
    has_openai = bool(client)
    return {
        "status": "healthy",
        "timestamp": __import__("datetime").datetime.now().isoformat(),
        "openai_status": "connected" if has_openai else "disconnected",
        "active_conversations": len(conversation_memory),
        "memory_usage": f"{len(str(conversation_memory)) / 1024:.2f} KB"
    }

@app.post("/api/chat")
async def chat_endpoint(request: Request):
    """پایانه مکالمه هوش مصنوعی"""
    try:
        data = await request.json()
        message = data.get("message", "").strip()
        session_id = data.get("session_id", "default")
        
        if not message:
            raise HTTPException(status_code=400, detail="پیام نمی‌تواند خالی باشد")
        
        logger.info(f"💬 درخواست چت: session={session_id}, length={len(message)}")
        
        # پاکسازی حافظه قدیمی
        cleanup_old_memory()
        
        # اندازه‌گیری زمان پاسخ
        import time
        start_time = time.time()
        
        # دریافت پاسخ از AI
        response = await call_openai(message, session_id)
        
        response_time = (time.time() - start_time) * 1000
        
        return {
            "success": True,
            "response": response,
            "session_id": session_id,
            "response_time": f"{response_time:.0f}ms",
            "model": "openai-gpt" if client else "fallback-model",
            "memory_size": len(conversation_memory.get(session_id, {}).get("history", [])) if session_id in conversation_memory else 0
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="فرمت JSON نامعتبر")
    except Exception as e:
        logger.error(f"❌ خطا در پردازش چت: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطای داخلی: {str(e)}")

@app.get("/api/status")
async def get_status():
    """وضعیت سیستم"""
    import platform
    import sys
    
    return {
        "system": {
            "python_version": sys.version,
            "platform": platform.platform(),
            "api_version": "1.5.0"
        },
        "ai": {
            "openai_configured": bool(OPENAI_API_KEY),
            "openai_connected": bool(client),
            "fallback_active": not bool(client)
        },
        "memory": {
            "active_sessions": len(conversation_memory),
            "total_messages": sum(len(m["history"]) for m in conversation_memory.values())
        }
    }

@app.post("/api/clear-memory")
async def clear_memory(session_id: Optional[str] = None):
    """پاکسازی حافظه"""
    if session_id:
        if session_id in conversation_memory:
            del conversation_memory[session_id]
            return {"success": True, "message": f"حافظه session {session_id} پاک شد"}
        else:
            raise HTTPException(status_code=404, detail="Session یافت نشد")
    else:
        conversation_memory.clear()
        return {"success": True, "message": "تمامی حافظه‌ها پاک شد"}

@app.get("/api/test-openai")
async def test_openai():
    """تست اتصال به OpenAI"""
    if not client:
        return {
            "success": False,
            "message": "OpenAI API Key تنظیم نشده است",
            "instruction": "لطفاً OPENAI_API_KEY را در Environment Variables تنظیم کنید"
        }
    
    try:
        test_prompt = "سلام! لطفاً یک جمله کوتاه فارسی بگو."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": test_prompt}],
            max_tokens=50
        )
        
        return {
            "success": True,
            "message": "OpenAI API متصل است",
            "test_response": response.choices[0].message.content,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"خطا در اتصال به OpenAI: {str(e)}",
            "error_type": type(e).__name__
        }

# ==================== مستندات ====================

SWAGGER_UI_HTML = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>ناطق اولتیمیت - مستندات API</title>
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
    <style>
        * { font-family: 'Vazirmatn', sans-serif !important; }
        body { margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; margin-bottom: 30px; background: linear-gradient(90deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .info-box { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 25px; }
        .status { padding: 10px 20px; border-radius: 20px; font-weight: bold; display: inline-block; margin: 10px 0; }
        .online { background: #2ecc71; color: white; }
        .offline { background: #e74c3c; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 ناطق اولتیمیت - مستندات هوش مصنوعی</h1>
        
        <div class="info-box">
            <h2>🔄 وضعیت سیستم</h2>
            <div id="status">در حال بررسی...</div>
            <p><strong>آدرس پایه:</strong> <code>https://natiq-ultimate.vercel.app/api</code></p>
            <p><strong>ورژن:</strong> 1.5.0</p>
        </div>
        
        <h2>📡 Endpointهای فعال</h2>
        <div id="swagger-ui"></div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-standalone-preset.js"></script>
    <script>
    window.onload = async function() {
        // بررسی وضعیت
        try {
            const status = await fetch('/api/status').then(r => r.json());
            const statusDiv = document.getElementById('status');
            if (status.ai.openai_connected) {
                statusDiv.innerHTML = '<span class="status online">✅ OpenAI متصل</span>';
            } else {
                statusDiv.innerHTML = '<span class="status offline">⚠️ حالت جایگزین فعال</span><br><small>برای اتصال به OpenAI، OPENAI_API_KEY را تنظیم کنید</small>';
            }
        } catch (e) {
            console.error(e);
        }
        
        // Swagger UI
        const ui = SwaggerUIBundle({
            url: "/api/openapi.json",
            dom_id: '#swagger-ui',
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIStandalonePreset
            ],
            layout: "StandaloneLayout",
            deepLinking: true,
            displayRequestDuration: true,
            docExpansion: 'list'
        });
        
        window.ui = ui;
    };
    </script>
</body>
</html>
"""

@app.get("/api/docs")
async def get_api_docs():
    """مستندات Swagger UI"""
    return HTMLResponse(content=SWAGGER_UI_HTML, status_code=200)

@app.get("/api/openapi.json")
async def get_openapi_spec():
    """OpenAPI Specification"""
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Natiq Ultimate AI API",
            "description": "هوش مصنوعی فارسی با قابلیت مکالمه و پردازش متن",
            "version": "1.5.0",
            "contact": {
                "name": "ناطق اولتیمیت",
                "url": "https://natiq-ultimate.vercel.app"
            }
        },
        "servers": [
            {
                "url": "https://natiq-ultimate.vercel.app/api",
                "description": "سرور تولید"
            }
        ],
        "paths": {
            "/chat": {
                "post": {
                    "summary": "مکالمه با هوش مصنوعی",
                    "description": "ارسال پیام و دریافت پاسخ از AI",
                    "requestBody": {
                        "required": true,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {
                                            "type": "string",
                                            "description": "پیام کاربر"
                                        },
                                        "session_id": {
                                            "type": "string",
                                            "description": "شناسه جلسه (اختیاری)"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "پاسخ موفق"
                        },
                        "400": {
                            "description": "پیام خالی یا نامعتبر"
                        }
                    }
                }
            }
        }
    }

# ==================== مدیریت خطا ====================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "مسیر یافت نشد",
            "path": str(request.url.path),
            "suggestion": "از endpoint /api/chat برای مکالمه با AI استفاده کنید"
        }
    )

# Middleware برای لاگ‌گیری
@app.middleware("http")
async def log_requests(request: Request, call_next):
    import time
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.0f}ms")
    
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=True
    )
