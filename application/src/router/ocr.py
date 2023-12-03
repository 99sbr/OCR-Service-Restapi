from fastapi import File, UploadFile, BackgroundTasks
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
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
    """
    Represents an image request.

    Attributes:
        data (str): The base64-encoded image data.

    Example:
        >>> image_data = "base64_encoded_data_here"
        >>> request = ImageRequest(data=image_data)
    """
    data: str

# A synchronous API that returns the extracted text given bs64 image


@router.post("/imgsync")
async def sync_text_extraction(image_request: ImageRequest):
    """
    Endpoint for synchronous text extraction from a provided image using OCR.

    Args:
        image_request (ImageRequest): An instance of the ImageRequest model containing the base64-encoded image data.

    Returns:
        JSONResponse: A JSON response containing the extracted text from the image.

    Example:
        >>> response = await sync_text_extraction(ImageRequest(data="base64_encoded_image_data_here"))
        >>> print(response.json())
        {"text": "extracted_text_here"}
    """
    logger.info(
        f'Received Request to Process Image for OCR at {datetime.datetime.now()}')
    text = await ocr_service.run_ocr(image_request.data)
    logger.info('Completed')
    return JSONResponse({"text": text})

# call the ocr service given job id and and bs64 data


async def run_ocr(data, job_id):
    text = await ocr_service.run_ocr(data)
    ocr_data.update({job_id: text})

# A asynchronous API that returns the jobID for the ocr-task given bs64 image


@router.post("/imgasync")
async def async_text_extraction(image_request: ImageRequest, background_tasks: BackgroundTasks):
    """
    Endpoint for asynchronous text extraction from a provided image using OCR.

    Args:
        image_request (ImageRequest): An instance of the ImageRequest model containing the base64-encoded image data.
        background_tasks (BackgroundTasks): An instance of BackgroundTasks for scheduling asynchronous tasks.

    Returns:
        dict: A dictionary containing the job_id for tracking the progress of the asynchronous task.

    Example:
        >>> response = await async_text_extraction(ImageRequest(data="base64_encoded_image_data_here"), background_tasks)
        >>> print(response)
        {"job_id": "generated_uuid_here"}
    """
    job_id = str(uuid4())
    background_tasks.add_task(run_ocr, image_request.data, job_id)
    return {"job_id": job_id}

# given a job id from imgasync, get the value of ocr text


@router.get("/ocr_text")
async def get_ocr_from_job_id(job_id: str):
    if job_id in ocr_data:
        text = ocr_data.get(job_id)
        return JSONResponse({"text": text})
    else:
        raise HTTPException(
            status_code=400, detail=f"Job ID: {job_id} does not exist.")
