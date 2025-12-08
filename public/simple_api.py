from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# فعال کردن CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "version": "6.0",
        "knowledge_count": 10,
        "message": "natiq-ultimate API"
    }

@app.get("/api/test")
async def test():
    return {"message": "Test successful"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8081)
