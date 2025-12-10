import asyncio
from fastapi import FastAPI
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

try:
    from app import app
except ImportError:
    app = FastAPI()
    
    @app.get("/")
    async def root():
        return {"message": "Natiq API"}

# Vercel به صورت خودکار app را به عنوان ASGI تشخیص می‌دهد
# نیازی به Mangum نیست
