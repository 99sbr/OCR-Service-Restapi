import os
import base64
import io
from PIL import Image
from application.main.config import settings


class BasicImageUtils:

    @classmethod
    async def decode_b64_image(cls, data,  cache=True):
        image_data = base64.b64decode(data)
        image = Image.open(io.BytesIO(image_data))
        if cache:
                image.save(os.path.join(settings.APP_CONFIG.CACHE_DIR, filename))
        return image

    # @classmethod
    # async def read_image_file(cls, file, filename, cache=True) -> Image.Image:
    #     image = Image.open(BytesIO(file))
    #     if cache:
    #         image.save(os.path.join(settings.APP_CONFIG.CACHE_DIR, filename))
    #     return image