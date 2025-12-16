from fastapi import APIRouter, BackgroundTasks
from app.core.database import SessionLocal
from app.models.media import MediaAsset
from app.services.analysis_task import run_caption_analysis

router = APIRouter(prefix="/analyze", tags=["Analyze"])

@router.post("/")
async def analyze(asset_id: str, background_tasks: BackgroundTasks):
    db = SessionLocal()
    asset = db.query(MediaAsset).filter(MediaAsset.id == asset_id).first()
    db.close()

    if not asset:
        return {"error": "Asset not found"}

    background_tasks.add_task(
        run_caption_analysis,
        asset.id,
        asset.s3_key
    )

    return {"status": "processing"}
