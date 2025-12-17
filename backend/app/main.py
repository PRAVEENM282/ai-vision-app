from fastapi import FastAPI
from app.routers import upload, analyze, generate
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="AI Vision App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your Next.js app
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (POST, GET, etc.)
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(analyze.router)
app.include_router(generate.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
