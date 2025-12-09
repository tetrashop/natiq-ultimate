#!/usr/bin/env python3
"""
فایل اصلی FastAPI برای پروژه natiq-ultimate
سازگار با Vercel Python Runtime
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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
app = FastAPI(
    title="Natiq Ultimate API",
    description="API برای پردازش متن و مدیریت فایل",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# تنظیم CORS برای Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        "docs": "/api/docs",
        "environment": os.getenv("VERCEL_ENV", "production"),
        "endpoints": {
            "health": "/api/health",
            "process": "/api/process",
            "file-info": "/api/file-info",
            "logs": "/api/logs"
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
        
        # اینجا منطق پردازش متن اضافه می‌شود
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
        # ایمپورت داینامیک برای جلوگیری از خطا در Vercel
        import sys
        sys.path.append(".")
        
        # بررسی وجود فایل
        file_path = Path(path)
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"فایل {path} یافت نشد"
            )
        
        # خواندن محتوای فایل
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # دریافت اطلاعات فایل
        stat = file_path.stat()
        
        return {
            "success": True,
            "file_path": str(file_path.absolute()),
            "file_name": file_path.name,
            "file_size": stat.st_size,
            "file_size_human": f"{stat.st_size / 1024:.2f} KB",
            "created_time": stat.st_ctime,
            "modified_time": stat.st_mtime,
            "content_preview": content[:500] + "..." if len(content) > 500 else content,
            "content_length": len(content),
            "is_file": file_path.is_file(),
            "is_directory": file_path.is_dir()
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
        log_file = "api.log"
        if not Path(log_file).exists():
            # ایجاد لاگ‌های نمونه
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
                "log_file_exists": False,
                "message": "فایل لاگ هنوز ایجاد نشده است. لاگ‌های نمونه نمایش داده می‌شوند."
            }
        
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # برگرداندن آخرین خطوط
        recent_logs = lines[-limit:] if len(lines) > limit else lines
        
        return {
            "success": True,
            "total_logs": len(lines),
            "recent_logs": recent_logs,
            "limit_applied": limit,
            "log_file_exists": True,
            "log_file_size": Path(log_file).stat().st_size
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
            "processor": platform.processor(),
            "system": platform.system(),
            "release": platform.release()
        },
        "api": {
            "version": "1.0.0",
            "environment": os.getenv("VERCEL_ENV", "production"),
            "base_url": os.getenv("VERCEL_URL", "https://natiq-ultimate.vercel.app")
        },
        "resources": {
            "memory": __import__("os").sysconf("SC_PAGE_SIZE") * __import__("os").sysconf("SC_PHYS_PAGES") if hasattr(__import__("os"), "sysconf") else "N/A",
            "cpus": __import__("os").cpu_count()
        }
    }

# ==================== هندلر خطاها ====================

@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    # اگر مسیر API نیست، فایل استاتیک برگردانیم
    if not request.url.path.startswith("/api/"):
        return FileResponse("public/index.html")
    
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
                "/api/system-info"
            ]
        }
    )

@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
    logger.error(f"خطای داخلی: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "خطای داخلی سرور",
            "message": "یک مشکل غیرمنتظره رخ داده است",
            "request_id": request.headers.get("x-vercel-id", "unknown")
        }
    )

# ==================== Middleware برای لاگ‌گیری ====================

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

# ==================== برای اجرای محلی ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=True
    )
