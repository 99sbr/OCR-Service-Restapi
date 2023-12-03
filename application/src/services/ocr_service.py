from fastapi.exceptions import HTTPException
from application.initializer import LoggerInstance
from application.src.utility.worker.image_utils import BasicImageUtils
from application.src.utility.worker.ocr_engine import OCREngine


class OCRService(object):
    """
    A service for Optical Character Recognition (OCR).

    Attributes:
        logger: LoggerInstance: An instance of the logger for logging information and errors.

    Methods:
        run_ocr(data: str) -> str:
            Runs OCR on the provided base64-encoded image data.

            Args:
                data (str): The base64-encoded image data.

            Returns:
                str: The extracted text from the image.

            Raises:
                HTTPException: If there are issues with decoding the image or running OCR.
    """

    def __init__(self):
        """
        Initializes the OCRService with a logger instance.
        """
        self.logger = LoggerInstance().get_logger(__name__)

    async def run_ocr(self, data):
        """
        Runs OCR on the provided base64-encoded image data.

        Args:
            data (str): The base64-encoded image data.

        Returns:
            str: The extracted text from the image.

        Raises:
            HTTPException: If there are issues with decoding the image or running OCR.
        """
        try:
            self.logger.info('Decoding Image')
            image = await BasicImageUtils.decode_b64_image(data)
        except Exception as e:
            self.logger.error(str(e))
            raise HTTPException(
                status_code=400, detail=f"Invalid image data: {e}")

        try:
            self.logger.info('Running OCR')
            text = await OCREngine.extract_text(image)
        except Exception as e:
            self.logger.error(str(e))
            raise HTTPException(
                status_code=500, detail=f"Error extracting text: {e}")

        return text
