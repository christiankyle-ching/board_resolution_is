from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

# Default values
MAX_RESOLUTION_PX = 2048
QUALITY = 85
FORMAT = "JPEG"


def compress_image(img, filename="image", image_format=FORMAT, quality=QUALITY, max_resolution=MAX_RESOLUTION_PX):
    filename = f"{filename}.{image_format}"

    # Containers
    compressed_img = Image.open(img)
    compressed_io = BytesIO()

    # Resize using thumbnail
    compressed_img.thumbnail(
        (max_resolution, max_resolution), resample=Image.ANTIALIAS)

    # If JPEG, we can't handle Alpha (RGBA)
    if image_format in ['JPEG']:
        compressed_img = compressed_img.convert('RGB')

    compressed_img.save(compressed_io, format=image_format, quality=quality)

    return InMemoryUploadedFile(compressed_io, None, filename,
                                f'image/{image_format.lower()}', compressed_io.tell(), None)
