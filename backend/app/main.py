from fastapi import FastAPI
from app.routers import upload, analyze

app = FastAPI(title="AI Vision App")

app.include_router(upload.router)
app.include_router(analyze.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
