import pytesseract
from application.initializer import LoggerInstance


class OCREngine:
    """
    A class representing an Optical Character Recognition (OCR) engine.

    Attributes:
        logger: logging.Logger: An instance of the logger for logging information and errors.

    Methods:
        extract_text(image) -> str:
            Extracts text from the provided image using OCR.

            Args:
                image: The image from which text needs to be extracted.

            Returns:
                str: The extracted text.

            Example:
                >>> ocr_engine = OCREngine()
                >>> image = ...  # Provide the actual image data or path
                >>> text = await ocr_engine.extract_text(image)
                >>> print(text)
                "Extracted text from the image."
    """
    logger = LoggerInstance().get_logger(__name__)

    @classmethod
    async def extract_text(cls, image):

        OCREngine.logger.info('Running OCR')
        text = pytesseract.image_to_string(image)
        OCREngine.logger.info('Completed OCR')
        return text
