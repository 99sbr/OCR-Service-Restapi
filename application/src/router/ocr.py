from fastapi import File, UploadFile, BackgroundTasks
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from PIL import Image
import datetime
from uuid import uuid4
from pydantic import BaseModel
from fastapi.exceptions import HTTPException
from application.initializer import LoggerInstance
from application.src.services.ocr_service import OCRService

router = APIRouter()
logger = LoggerInstance().get_logger(__name__)
ocr_service = OCRService()

ocr_data = dict()

class ImageRequest(BaseModel):
    data: str

@router.post("/imgsync")
async def sync_text_extraction(image_request: ImageRequest):
    logger.info(f'Received Request to Process Image for OCR at {datetime.datetime.now()}')
    text = await ocr_service.run_ocr(image_request.data)
    logger.info('Completed')
    return JSONResponse({"text": text})

async def run_ocr(data, job_id):
    text = await ocr_service.run_ocr(data)
    ocr_data.update({job_id: text})

@router.post("/imgasync")
async def async_text_extraction(image_request: ImageRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid4())
    background_tasks.add_task(run_ocr,image_request.data, job_id)
    return {"job_id": job_id}


@router.get("/ocr_text")
async def get_ocr_from_job_id(job_id: str):
    if job_id in ocr_data:
        text = ocr_data.get(job_id)
        return JSONResponse({"text": text})
    else:
        raise HTTPException(status_code=400, detail=f"Job ID: {job_id} does not exist.")