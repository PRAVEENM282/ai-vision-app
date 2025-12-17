from fastapi import APIRouter, BackgroundTasks
from app.core.database import SessionLocal
from app.models.media import MediaAsset
from app.models.analysis import AnalysisResult
from app.services.analysis_task import run_caption_analysis

router = APIRouter(prefix="/api/analyze", tags=["Analyze"])


@router.post("/caption")
def caption(asset_id: str, background_tasks: BackgroundTasks):
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


@router.get("/result")
def get_analysis_result(asset_id: str, feature_type: str):
    db = SessionLocal()

    result = (
        db.query(AnalysisResult)
        .filter(
            AnalysisResult.asset_id == asset_id,
            AnalysisResult.feature_type == feature_type,
        )
        .order_by(AnalysisResult.created_at.desc())
        .first()
    )

    db.close()

    if not result:
        return {"status": "processing"}

    if result.result_data.get("status") == "failed":
        return {
            "status": "failed",
            "error": result.result_data.get("error"),
        }

    return {
        "status": "completed",
        "result": result.result_data,
    }
