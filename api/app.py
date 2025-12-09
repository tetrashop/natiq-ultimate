#!/usr/bin/env python3
"""
فایل اصلی FastAPI برای پروژه natiq-ultimate
سازگار با Vercel Python Runtime
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import json
from pathlib import Path
from typing import Optional

# تنظیمات لاگ‌گیری برای Vercel
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ایجاد نمونه اصلی FastAPI
# غیرفعال کردن مستندات خودکار FastAPI
app = FastAPI(
    title="Natiq Ultimate API",
    description="API برای پردازش متن و مدیریت فایل",
    version="1.0.0",
    docs_url=None,  # غیرفعال
    redoc_url=None,  # غیرفعال
    openapi_url="/api/openapi.json"  # فقط OpenAPI JSON
)

# تنظیم CORS برای Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== مستندات دستی ====================

SWAGGER_UI_HTML = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Natiq Ultimate API - مستندات</title>
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
    <style>
        * { font-family: 'Vazirmatn', sans-serif !important; }
        body { margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; margin-bottom: 30px; }
        .info-box { background: #e8f4fd; padding: 15px; border-radius: 5px; margin-bottom: 20px; border-right: 4px solid #1890ff; }
        .endpoint-list { list-style: none; padding: 0; }
        .endpoint-list li { padding: 10px; border-bottom: 1px solid #eee; }
        .method { display: inline-block; padding: 4px 8px; border-radius: 4px; font-weight: bold; margin-left: 10px; }
        .get { background: #61affe; color: white; }
        .post { background: #49cc90; color: white; }
        .put { background: #fca130; color: white; }
        .delete { background: #f93e3e; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 مستندات Natiq Ultimate API</h1>
        
        <div class="info-box">
            <strong>آدرس پایه:</strong> <code>https://natiq-ultimate.vercel.app/api</code><br>
            <strong>ورژن:</strong> 1.0.0<br>
            <strong>محیط:</strong> production
        </div>
        
        <h2>📋 لیست Endpointها</h2>
        <ul class="endpoint-list">
            <li>
                <span class="method get">GET</span>
                <code>/api/</code> - اطلاعات کلی API
            </li>
            <li>
                <span class="method get">GET</span>
                <code>/api/health</code> - بررسی سلامت API
            </li>
            <li>
                <span class="method post">POST</span>
                <code>/api/process</code> - پردازش متن
            </li>
            <li>
                <span class="method get">GET</span>
                <code>/api/file-info</code> - اطلاعات فایل
            </li>
            <li>
                <span class="method get">GET</span>
                <code>/api/logs</code> - لاگ‌های سیستم
            </li>
            <li>
                <span class="method get">GET</span>
                <code>/api/system-info</code> - اطلاعات سیستم
            </li>
            <li>
                <span class="method get">GET</span>
                <code>/api/openapi.json</code> - OpenAPI Spec
            </li>
        </ul>
        
        <h2>🔧 تست سریع API</h2>
        <div id="swagger-ui"></div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-standalone-preset.js"></script>
    <script>
    window.onload = function() {
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

REDOC_HTML = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Natiq Ultimate API - مستندات ReDoc</title>
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    <style>
        body { margin: 0; padding: 0; }
        .header { background: #333; color: white; padding: 20px; text-align: center; }
        .header h1 { margin: 0; font-family: 'Vazirmatn', sans-serif; }
        .info { padding: 20px; background: #f5f5f5; text-align: center; font-family: 'Vazirmatn', sans-serif; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Natiq Ultimate API - مستندات ReDoc</h1>
    </div>
    <div class="info">
        <p>در حال بارگذاری مستندات...</p>
        <p>اگر مستندات نمایش داده نمی‌شود، <a href="/api/openapi.json">این فایل JSON</a> را مستقیماً بررسی کنید.</p>
    </div>
    <redoc spec-url="/api/openapi.json"></redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"></script>
</body>
</html>
"""

# ==================== مسیرهای اصلی API ====================

@app.get("/")
async def root():
    """صفحه اصلی - هدایت به رابط کاربری"""
    return FileResponse("public/index.html")

@app.get("/api/")
async def api_root():
    """بررسی وضعیت سرور API"""
    return {
        "message": "خوش آمدید به Natiq Ultimate API",
        "status": "active",
        "version": "1.0.0",
        "environment": os.getenv("VERCEL_ENV", "production"),
        "endpoints": {
            "health": "/api/health",
            "process": "/api/process",
            "file-info": "/api/file-info",
            "logs": "/api/logs",
            "system-info": "/api/system-info",
            "openapi": "/api/openapi.json",
            "docs": "/api/docs",
            "redoc": "/api/redoc"
        }
    }

@app.get("/api/health")
async def health_check():
    """بررسی سلامت API"""
    return {
        "status": "healthy",
        "timestamp": __import__("datetime").datetime.now().isoformat(),
        "service": "natiq-ultimate-api",
        "version": "1.0.0"
    }

@app.post("/api/process")
async def process_text(request: Request):
    """
    پردازش متن ورودی کاربر
    """
    try:
        body = await request.json()
        text = body.get("text", "").strip()
        
        if not text:
            raise HTTPException(
                status_code=400,
                detail="متن ورودی نمی‌تواند خالی باشد"
            )
        
        logger.info(f"درخواست پردازش متن دریافت شد. طول متن: {len(text)}")
        
        processed_text = f"پردازش شده: {text[:50]}..." if len(text) > 50 else f"پردازش شده: {text}"
        
        return {
            "success": True,
            "original_length": len(text),
            "processed_text": processed_text,
            "message": "پردازش با موفقیت انجام شد",
            "language": "fa",
            "char_count": len(text),
            "word_count": len(text.split())
        }
        
    except HTTPException:
        raise
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="فرمت JSON نامعتبر است"
        )
    except Exception as e:
        logger.error(f"خطا در پردازش متن: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="خطای داخلی سرور در پردازش متن"
        )

@app.get("/api/file-info")
async def get_file_info(path: str = "requirements.txt"):
    """
    دریافت اطلاعات یک فایل
    """
    try:
        file_path = Path("/var/task") / path
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"فایل {path} یافت نشد"
            )
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        stat = file_path.stat()
        
        return {
            "success": True,
            "file_path": str(file_path),
            "file_name": file_path.name,
            "file_size": stat.st_size,
            "file_size_human": f"{stat.st_size / 1024:.2f} KB",
            "content_preview": content[:500] + "..." if len(content) > 500 else content,
            "content_length": len(content),
            "is_file": file_path.is_file()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطا در خواندن فایل {path}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"خطا در خواندن فایل: {str(e)}"
        )

@app.get("/api/logs")
async def get_logs(limit: int = 50):
    """
    دریافت آخرین لاگ‌های سیستم
    """
    try:
        log_file = Path("/var/task/api.log")
        if not log_file.exists():
            sample_logs = [
                f"{__import__('datetime').datetime.now().isoformat()} - INFO - API شروع شد",
                f"{__import__('datetime').datetime.now().isoformat()} - INFO - درخواست سلامت دریافت شد",
                f"{__import__('datetime').datetime.now().isoformat()} - INFO - سیستم آماده به کار است"
            ]
            
            return {
                "success": True,
                "total_logs": len(sample_logs),
                "recent_logs": sample_logs[-limit:],
                "limit_applied": limit,
                "log_file_exists": False
            }
        
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        recent_logs = lines[-limit:] if len(lines) > limit else lines
        
        return {
            "success": True,
            "total_logs": len(lines),
            "recent_logs": recent_logs,
            "limit_applied": limit,
            "log_file_exists": True,
            "log_file_size": log_file.stat().st_size
        }
        
    except Exception as e:
        logger.error(f"خطا در خواندن لاگ‌ها: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="خطا در دریافت لاگ‌های سیستم"
        )

@app.get("/api/system-info")
async def get_system_info():
    """
    دریافت اطلاعات سیستم
    """
    import platform
    import sys
    
    return {
        "success": True,
        "system": {
            "python_version": sys.version,
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release()
        },
        "api": {
            "version": "1.0.0",
            "environment": os.getenv("VERCEL_ENV", "production"),
            "base_url": os.getenv("VERCEL_URL", "https://natiq-ultimate.vercel.app")
        },
        "resources": {
            "cpus": os.cpu_count()
        }
    }

# ==================== مستندات API ====================

@app.get("/api/openapi.json")
async def get_openapi_spec():
    """OpenAPI Specification"""
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Natiq Ultimate API",
            "description": "API برای پردازش متن و مدیریت فایل",
            "version": "1.0.0"
        },
        "servers": [
            {
                "url": "https://natiq-ultimate.vercel.app/api",
                "description": "Production server"
            }
        ],
        "paths": {
            "/": {
                "get": {
                    "summary": "اطلاعات کلی API",
                    "responses": {
                        "200": {
                            "description": "موفق"
                        }
                    }
                }
            },
            "/health": {
                "get": {
                    "summary": "بررسی سلامت API",
                    "responses": {
                        "200": {
                            "description": "API سالم است"
                        }
                    }
                }
            },
            "/process": {
                "post": {
                    "summary": "پردازش متن",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "text": {
                                            "type": "string",
                                            "description": "متن ورودی"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "متن با موفقیت پردازش شد"
                        },
                        "400": {
                            "description": "خطا در درخواست"
                        }
                    }
                }
            },
            "/file-info": {
                "get": {
                    "summary": "اطلاعات فایل",
                    "parameters": [
                        {
                            "name": "path",
                            "in": "query",
                            "required": False,
                            "schema": {
                                "type": "string"
                            },
                            "description": "مسیر فایل",
                            "default": "requirements.txt"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "اطلاعات فایل"
                        },
                        "404": {
                            "description": "فایل یافت نشد"
                        }
                    }
                }
            },
            "/logs": {
                "get": {
                    "summary": "لاگ‌های سیستم",
                    "parameters": [
                        {
                            "name": "limit",
                            "in": "query",
                            "required": False,
                            "schema": {
                                "type": "integer"
                            },
                            "description": "تعداد لاگ‌ها",
                            "default": 50
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "لیست لاگ‌ها"
                        }
                    }
                }
            },
            "/system-info": {
                "get": {
                    "summary": "اطلاعات سیستم",
                    "responses": {
                        "200": {
                            "description": "اطلاعات سیستم"
                        }
                    }
                }
            }
        }
    }

@app.get("/api/docs")
async def get_api_docs():
    """مستندات Swagger UI"""
    return HTMLResponse(content=SWAGGER_UI_HTML, status_code=200)

@app.get("/api/redoc")
async def get_api_redoc():
    """مستندات ReDoc"""
    return HTMLResponse(content=REDOC_HTML, status_code=200)

@app.get("/docs")
async def redirect_to_docs():
    """هدایت به مستندات"""
    return RedirectResponse(url="/api/docs")

@app.get("/redoc")
async def redirect_to_redoc():
    """هدایت به ReDoc"""
    return RedirectResponse(url="/api/redoc")

# ==================== هندلر خطاها ====================

@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "مسیر یافت نشد",
            "path": str(request.url.path),
            "available_endpoints": [
                "/api/",
                "/api/health",
                "/api/process",
                "/api/file-info",
                "/api/logs",
                "/api/system-info",
                "/api/docs",
                "/api/redoc",
                "/api/openapi.json"
            ]
        }
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = __import__("time").time()
    
    response = await call_next(request)
    
    process_time = (__import__("time").time() - start_time) * 1000
    formatted_process_time = f"{process_time:.2f}ms"
    
    logger.info(
        f"{request.method} {request.url.path} "
        f"completed in {formatted_process_time} "
        f"status: {response.status_code}"
    )
    
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=True
    )
