from fastapi import File, UploadFile, BackgroundTasks
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from PIL import Image
import datetime
from pydantic import BaseModel
from application.initializer import LoggerInstance
from application.src.services.ocr_service import OCRService

router = APIRouter()
logger = LoggerInstance().get_logger(__name__)
ocr_service = OCRService()


class ImageRequest(BaseModel):
    data: str

@router.post("/imgsync")
async def sync_text_extraction(image_request: ImageRequest):
    logger.info(f'Received Request to Process Image for OCR at {datetime.datetime.now()}')
    text = await ocr_service.run_ocr(image_request.data)
    logger.info('Completed')
    return JSONResponse({"text": text})


# @router.post("/imgsync")
# async def async_text_extraction(data: str, background_tasks: BackgroundTasks):
#     job_id = await create_job(data)
#     text = await get_text(job_id)
#     return {"job_id": job_id, "text": text}