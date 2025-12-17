from fastapi import FastAPI
from app.routers import upload, analyze, generate

app = FastAPI(title="AI Vision App")

app.include_router(upload.router)
app.include_router(analyze.router)
app.include_router(generate.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
