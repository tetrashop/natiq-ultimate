
from fastapi import FastAPI, HTTPException, Query, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import json
import os
import sys
import logging
from typing import Optional, List
import asyncio
from contextlib import asynccontextmanager

# اضافه کردن مسیر src به sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# تنظیمات logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# مدل‌های درخواست
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 500

class BatchRequest(BaseModel):
    messages: List[str]
    session_id: Optional[str] = None

class ModelLoadRequest(BaseModel):
    model_name: str = "HooshvareLab/bert-base-parsbert-uncased"
    use_local: bool = True

@asynccontextmanager
async def lifespan(app: FastAPI):
    """مدیریت lifecycle برنامه"""
    logger.info("🚀 راه‌اندازی برنامه FastAPI")
    
    # بارگذاری مدل به صورت lazy (هنگام اولین درخواست)
    app.state.model_loaded = False
    app.state.nlp_processor = None
    
    yield
    
    # Cleanup
    logger.info("🔴 خاموش کردن برنامه")
    if app.state.nlp_processor:
        # ذخیره حالت مدل
        try:
            app.state.nlp_processor.save_model_locally()
        except:
            pass

# ایجاد برنامه FastAPI
app = FastAPI(
    title="natiq-ultimate API",
    description="API هوش مصنوعی پردازش زبان فارسی",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ذخیره‌سازی موقت برای sessions
app.state.sessions = {}

def load_nlp_processor():
    """بارگذاری پردازشگر NLP (lazy loading)"""
    if not app.state.model_loaded or app.state.nlp_processor is None:
        try:
            from src.core.nlp_processor import NLPProcessor
            from src.config import settings
            
            logger.info("در حال بارگذاری مدل NLP...")
            
            # تنظیم مسیر کش برای Vercel
            cache_dir = os.getenv("MODEL_CACHE_DIR", "/tmp/natiq-models")
            settings["model"].LOCAL_MODEL_PATH = cache_dir
            
            app.state.nlp_processor = NLPProcessor()
            app.state.model_loaded = True
            logger.info("✅ مدل NLP بارگذاری شد")
            
        except Exception as e:
            logger.error(f"خطا در بارگذاری مدل: {e}")
            raise HTTPException(status_code=500, detail=f"خطا در بارگذاری مدل: {str(e)}")
    
    return app.state.nlp_processor

# Routes
@app.get("/")
async def root():
    """صفحه اصلی"""
    return {
        "message": "خوش آمدید به natiq-ultimate API",
        "version": "1.0.0",
        "status": "فعال",
        "endpoints": {
            "chat": "/api/chat",
            "batch": "/api/batch",
            "health": "/api/health",
            "load_model": "/api/load-model"
        }
    }

@app.get("/api/health")
async def health_check():
    """بررسی سلامت API"""
    try:
        processor = load_nlp_processor()
        return {
            "status": "healthy",
            "model_loaded": app.state.model_loaded,
            "environment": os.getenv("VERCEL_ENV", "development"),
            "python_version": sys.version
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """پردازش پیام متنی"""
    try:
        processor = load_nlp_processor()
        
        logger.info(f"دریافت پیام: {request.message[:50]}...")
        
        # پردازش متن
        result = processor.process(request.message)
        
        # ذخیره در session (اگر session_id وجود دارد)
        if request.session_id:
            if request.session_id not in app.state.sessions:
                app.state.sessions[request.session_id] = []
            app.state.sessions[request.session_id].append({
                "message": request.message,
                "response": result,
                "timestamp": asyncio.get_event_loop().time()
            })
        
        return {
            "success": True,
            "response": result.get("fallback_response") if "error" in result else result,
            "session_id": request.session_id,
            "processing_time": result.get("processing_time", 0)
        }
        
    except Exception as e:
        logger.error(f"خطا در پردازش پیام: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/batch")
async def batch_endpoint(request: BatchRequest):
    """پردازش دسته‌ای متون"""
    try:
        processor = load_nlp_processor()
        
        logger.info(f"دریافت {len(request.messages)} پیام برای پردازش دسته‌ای")
        
        results = []
        for i, message in enumerate(request.messages):
            result = processor.process(message)
            results.append({
                "index": i,
                "message": message,
                "result": result
            })
        
        return {
            "success": True,
            "total": len(results),
            "results": results,
            "session_id": request.session_id
        }
        
    except Exception as e:
        logger.error(f"خطا در پردازش دسته‌ای: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/load-model")
async def load_model_endpoint(request: ModelLoadRequest):
    """بارگذاری مدل جدید"""
    try:
        from src.core.nlp_processor import NLPProcessor
        
        logger.info(f"درخواست بارگذاری مدل: {request.model_name}")
        
        # بارگذاری مدل جدید
        processor = NLPProcessor(model_name=request.model_name)
        app.state.nlp_processor = processor
        app.state.model_loaded = True
        
        return {
            "success": True,
            "message": f"مدل {request.model_name} با موفقیت بارگذاری شد",
            "model_name": request.model_name
        }
        
    except Exception as e:
        logger.error(f"خطا در بارگذاری مدل: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """دریافت تاریخچه session"""
    if session_id in app.state.sessions:
        return {
            "success": True,
            "session_id": session_id,
            "messages": app.state.sessions[session_id],
            "count": len(app.state.sessions[session_id])
        }
    else:
        return {
            "success": False,
            "message": "Session not found"
        }

# برای Vercel Serverless
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
