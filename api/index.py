from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.post("/api/ask")
def ask_question(question: dict):
    try:
        q = question.get("question", "").strip()
        
        # پاسخ ساده
        response = f"شما پرسیدید: '{q}'. پاسخ از natiq-ultimate v6.0"
        
        return {
            "success": True,
            "response": response,
            "question": q
        }
    except:
        return {"success": False, "response": "خطا در پردازش"}

@app.get("/api/test")
def test():
    return {"message": "API کار می‌کند"}
