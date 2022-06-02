from io import BytesIO
from PIL import Image
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from resolutions.models import Certificate, CertificateImage, Resolution

import pytesseract
OCR_TIMEOUT = 5


@receiver(post_save, sender=Certificate)
def certificate_delete_resolutions_images(sender, instance, created, **kwargs):
    if not created:
        if not instance.active:
            for res in instance.resolutions:
                res.delete()
            for img in instance.images:
                img.delete()


@receiver(post_save, sender=Resolution)
def last_resolution_delete_certificate(sender, instance, created, *args, **kwargs):
    if not created:
        if not instance.active:
            remaining_res = instance.certificate.resolutions.count()
            if remaining_res <= 0 and instance.certificate.active:
                instance.certificate.delete()


# @receiver(post_save, sender=CertificateImage)
# def read_image_ocr(sender, instance, created, *args, **kwargs):
#     if created and instance.image:
#         pilImage = Image.open(BytesIO(instance.image.read()))

#         # # Try read image for keywords
#         _ocr = ''
#         try:
#             _ocr = pytesseract.image_to_string(
#                 pilImage, timeout=OCR_TIMEOUT)
#             print("OCR: " + _ocr)
#         except Exception as e:
#             print(f'OCR Error: Cannot read text - {e}')
#             pass

#         instance.ocr = _ocr
#         instance.save(update_fields=['ocr'])
