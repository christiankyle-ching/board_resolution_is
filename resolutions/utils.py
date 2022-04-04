from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

MAX_RESOLUTION_PX = 2048
JPEG_QUALITY = 85


def compress_image(img, filename="image.JPG"):
    compressed_img = Image.open(img)
    compressed_io = BytesIO()

    compressed_img.thumbnail(
        (MAX_RESOLUTION_PX, MAX_RESOLUTION_PX), resample=Image.ANTIALIAS)
    compressed_img = compressed_img.convert('RGB')
    compressed_img.save(compressed_io, format='JPEG', quality=JPEG_QUALITY)

    return InMemoryUploadedFile(compressed_io, None, filename,
                                'image/jpeg', compressed_io.tell(), None)
