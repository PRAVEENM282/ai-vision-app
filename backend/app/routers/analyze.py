from fastapi import APIRouter, BackgroundTasks
from app.core.database import SessionLocal
from app.models.media import MediaAsset
from app.services.analysis_task import (
    run_caption_analysis,
    run_vqa_analysis,
    run_ocr_analysis,
)

router = APIRouter(prefix="/api/analyze", tags=["Analyze"])


@router.post("/caption")
async def caption(asset_id: str, background_tasks: BackgroundTasks):
    db = SessionLocal()
    asset = db.query(MediaAsset).filter(MediaAsset.id == asset_id).first()
    db.close()

    if not asset:
        return {"error": "Asset not found"}

    background_tasks.add_task(
        run_caption_analysis,
        asset.id,
        asset.s3_key,
    )

    return {"status": "caption processing started"}


@router.post("/vqa")
async def vqa(
    asset_id: str,
    question: str,
    background_tasks: BackgroundTasks,
):
    db = SessionLocal()
    asset = db.query(MediaAsset).filter(MediaAsset.id == asset_id).first()
    db.close()

    if not asset:
        return {"error": "Asset not found"}

    background_tasks.add_task(
        run_vqa_analysis,
        asset.id,
        asset.s3_key,
        question,
    )

    return {"status": "vqa processing started"}


@router.post("/ocr")
async def ocr(asset_id: str, background_tasks: BackgroundTasks):
    db = SessionLocal()
    asset = db.query(MediaAsset).filter(MediaAsset.id == asset_id).first()
    db.close()

    if not asset:
        return {"error": "Asset not found"}

    background_tasks.add_task(
        run_ocr_analysis,
        asset.id,
        asset.s3_key,
    )

    return {"status": "ocr processing started"}
