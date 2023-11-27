from fastapi import File, UploadFile, BackgroundTasks
from fastapi.routing import APIRouter

from PIL import Image
import pytesseract

from application.initializer import LoggerInstance
from application.main.services.ocr_service import OCRService
from application.main.utility.manager.image_utils import BasicImageUtils


router = APIRouter()
logger = LoggerInstance().get_logger(__name__)


@router.post("/imgsync")
async def sync_text_extraction(data: str):
    image = decode_b64_image(data)
    text = await extract_text(image)
    return {"text": text}


@router.post("/imgsync")
async def async_text_extraction(data: str, background_tasks: BackgroundTasks):
    job_id = await create_job(data)
    text = await get_text(job_id)
    return {"job_id": job_id, "text": text}