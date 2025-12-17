import asyncio
from app.core.database import SessionLocal
from app.models.analysis import AnalysisResult
from app.services.s3_service import generate_presigned_url
from app.services.vision_service import analyze_image

def run_caption_analysis(asset_id, s3_key):
    db = SessionLocal()

    try:
        image_url = generate_presigned_url(s3_key)
        prompt = "Describe the image clearly."

        # Run async function properly
        result_text = asyncio.run(
            analyze_image(image_url, prompt)
        )

        analysis = AnalysisResult(
            asset_id=asset_id,
            feature_type="caption",
            prompt_text=prompt,
            result_data={"text": result_text}
        )

        db.add(analysis)
        db.commit()
    finally:
        db.close()

def run_vqa_analysis(asset_id, s3_key, question):
    db = SessionLocal()

    try:
        image_url = generate_presigned_url(s3_key)
        prompt = f"Answer the question based only on the image: {question}"

        result_text = asyncio.run(
            analyze_image(image_url, prompt)
        )

        analysis = AnalysisResult(
            asset_id=asset_id,
            feature_type="vqa",
            prompt_text=question,
            result_data={"answer": result_text}
        )

        db.add(analysis)
        db.commit()
    finally:
        db.close()


def run_ocr_analysis(asset_id, s3_key):
    db = SessionLocal()

    try:
        image_url = generate_presigned_url(s3_key)
        prompt = "Extract all visible text from the image."

        result_text = asyncio.run(
            analyze_image(image_url, prompt)
        )

        analysis = AnalysisResult(
            asset_id=asset_id,
            feature_type="ocr",
            prompt_text=prompt,
            result_data={"text": result_text}
        )

        db.add(analysis)
        db.commit()
    finally:
        db.close()
