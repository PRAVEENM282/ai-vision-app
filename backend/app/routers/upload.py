from fastapi import APIRouter, UploadFile, File
from app.services.s3_service import upload_file, generate_presigned_url
from app.core.database import SessionLocal
from app.models.media import MediaAsset

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/")
async def upload_image(file: UploadFile = File(...)):
    content = await file.read()

    s3_key = upload_file(content, file.content_type)

    # Generate TEMP URL for immediate use
    presigned_url = generate_presigned_url(s3_key)

    db = SessionLocal()
    asset = MediaAsset(
        s3_key=s3_key,
        s3_url=presigned_url,  # optional cache
        media_type=file.content_type,
        origin="uploaded"
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    db.close()

    return {
        "asset_id": asset.id,
        "s3_key": s3_key,
        "url": presigned_url
    }
