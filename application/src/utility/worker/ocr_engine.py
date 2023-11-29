import pytesseract
from PIL import Image
from application.initializer import LoggerInstance

class OCREngine:
    logger = LoggerInstance().get_logger(__name__)
    @classmethod
    async def extract_text(cls, image):
        OCREngine.logger.info('Running OCR')
        text = pytesseract.image_to_string(image)
        OCREngine.logger.info('Completed OCR')
        return text