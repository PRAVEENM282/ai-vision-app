from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.generation_service import (
    generate_image_from_text,
    generate_variation
)

router = APIRouter(prefix="/api/generate", tags=["Generation"])

@router.post("/text-to-image")
def text_to_image(prompt: str, db: Session = Depends(get_db)):
    return generate_image_from_text(prompt, db)

@router.post("/variation")
def variation(image_url: str, prompt: str, db: Session = Depends(get_db)):
    return generate_variation(image_url, prompt, db)
