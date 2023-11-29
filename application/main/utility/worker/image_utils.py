import os
import base64
import io
from uuid import uuid4
from PIL import Image
from application.initializer import LoggerInstance
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class BasicImageUtils:
    logger = LoggerInstance().get_logger(__name__)

    @classmethod
    async def decode_b64_image(cls, data,  cache=False):
        
        image_data = base64.b64decode(data)
        image = Image.open(io.BytesIO(image_data))
        filename = str(uuid4()) + '.jpg'
        if cache:
                img_save_path = os.path.join(os.environ['IMAGE_CACHE_FOLDER'], filename)
                image.save(img_save_path)
                BasicImageUtils.logger.info(f'Image Cached at: {img_save_path}')
        return image

    # @classmethod
    # async def read_image_file(cls, file, filename, cache=True) -> Image.Image:
    #     image = Image.open(BytesIO(file))
    #     if cache:
    #         image.save(os.path.join(settings.APP_CONFIG.CACHE_DIR, filename))
    #     return image