from fastapi.exceptions import HTTPException
from application.initializer import LoggerInstance
from application.src.utility.worker.image_utils import BasicImageUtils
from application.src.utility.worker.ocr_engine import OCREngine



class OCRService(object):

    def __init__(self):
        self.logger = LoggerInstance().get_logger(__name__)

    async def run_ocr(self, data):
        try:
            self.logger.info('Decoding Image')
            image = await BasicImageUtils.decode_b64_image(data)
        except Exception as e:
            self.logger.error(str(e))
            raise HTTPException(status_code=400, detail=f"Invalid image data: {e}")
        
        try:
            self.logger.info('Running OCR')
            text = await OCREngine.extract_text(image)
        except Exception as e:
            self.logger.error(str(e))
            raise HTTPException(status_code=500, detail=f"Error extracting text: {e}")
        
        return text