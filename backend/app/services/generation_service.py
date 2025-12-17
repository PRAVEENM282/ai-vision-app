import os
import uuid
import requests
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.models.media import MediaAsset
from app.models.generation import GenerationLog
from app.services.s3_service import upload_bytes

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

HF_MODEL_URL = (
    "https://router.huggingface.co/hf-inference/models/"
    "stabilityai/stable-diffusion-xl-base-1.0"
)


HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Accept": "image/png",
    "Content-Type": "application/json",
}


def generate_image_from_text(prompt: str, db: Session):
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True},
    }

    response = requests.post(
        HF_MODEL_URL,
        headers=HEADERS,
        json=payload,
        timeout=120,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"HuggingFace API error: {response.text}"
        )

    image_bytes = response.content

    s3_key = f"generated/{uuid.uuid4()}.png"
    upload_bytes(image_bytes, s3_key, "image/png")

    s3_url = f"https://{os.getenv('AWS_BUCKET_NAME')}.s3.amazonaws.com/{s3_key}"

    media = MediaAsset(
        s3_key=s3_key,
        s3_url=s3_url,
        media_type="image/png",
        origin="generated",
    )

    db.add(media)
    db.commit()
    db.refresh(media)

    log = GenerationLog(
        generated_asset_id=media.id,
        prompt=prompt,
        model_used="stable-diffusion-xl",
    )

    db.add(log)
    db.commit()

    return {
        "asset_id": str(media.id),
        "image_url": s3_url,
    }


def generate_variation(image_url: str, prompt: str, db: Session):
    combined_prompt = (
        f"Create a variation of this image: {image_url}. {prompt}"
    )

    return generate_image_from_text(combined_prompt, db)
