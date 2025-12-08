from fastapi import FastAPI

app = FastAPI()

@app.get("/api/health")
def health():
    return {"status": "healthy"}

@app.get("/")
def root():
    return {"message": "Use /api/ask endpoint for chat"}
