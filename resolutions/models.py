import re
import pytesseract
from PIL import Image, ImageOps, ExifTags
from io import BytesIO
from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.core.files import File

from board_resolution_is import abstract_models

_User = get_user_model()


class Certificate(abstract_models.NoDeleteModel, abstract_models.AddedByModel):
    # added_by = models.ForeignKey(_User, null=True, on_delete=models.SET_NULL)
    # added_date = models.DateTimeField(null=False, default=timezone.now)

    is_minutes_of_meeting = models.BooleanField(default=False)
    date_approved = models.DateField(blank=False, null=False)
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ['-added_date']

    @property
    def resolutions(self):
        return Resolution.objects.filter(certificate=self).order_by('number')

    @property
    def images(self):
        return CertificateImage.objects.filter(certificate=self)

    @property
    def label(self):
        return "Minutes of Meeting" if self.is_minutes_of_meeting else "Certificate"

    def __str__(self):
        return f"{self.label} #{self.pk}"

    def get_absolute_url(self):
        return reverse("resolutions:cert_detail", kwargs={'pk': self.pk})


class Resolution(abstract_models.NoDeleteModel, abstract_models.AddedByModel):
    # added_date = models.DateTimeField(null=False, default=timezone.now)

    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)

    number = models.CharField(max_length=50, blank=False, null=False)
    title = models.TextField(blank=False, null=False)

    class Meta:
        ordering = ['-added_date']

    def __str__(self):
        return f"Res. No. {self.number} - {self.title}"

    def get_absolute_url(self):
        return reverse("resolutions:cert_detail", kwargs={'pk': self.certificate.pk})


OCR_TIMEOUT = 5


class CertificateImage(abstract_models.NoDeleteModel):
    def certificate_image_path(instance, filename):
        return f"certificates/cert-{instance.certificate.id}/{filename}"

    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)

    image = models.ImageField(upload_to=certificate_image_path)
    ocr = models.TextField(blank=True, null=False, default="")

    def __str__(self):
        return self.image.name

    class Meta:
        ordering = ['image']

    def get_absolute_url(self):
        return reverse('resolutions:cert_detail', kwargs={'pk': self.certificate.pk})

    def save(self, use_ocr=False, *args, **kwargs):
        if self.image:
            pilImage = Image.open(BytesIO(self.image.read()))
            output = BytesIO()

            print("Process Image EXIF")
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break

                exif = pilImage._getexif()

                if exif[orientation] == 3:
                    pilImage = pilImage.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    pilImage = pilImage.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    pilImage = pilImage.rotate(90, expand=True)
            except Exception as e:
                print(f"No EXIF Data: {e}")

            # Try read image for keywords
            if use_ocr:
                try:
                    _ocr = pytesseract.image_to_string(
                        pilImage, timeout=OCR_TIMEOUT)
                    self.ocr = get_utf_safe_str(_ocr)
                    print("OCR: " + _ocr)
                except Exception as e:
                    print(f'OCR Error: Cannot read text - {e}')
                    pass

            pilImage.convert("RGB").save(output, format="JPEG", quality=75)
            output.seek(0)
            self.image = File(output, self.image.name)

        return super().save(*args, **kwargs)


def get_utf_safe_str(str):
    pattern = re.compile(r'[^a-zA-Z0-9 ]+', re.UNICODE)
    return pattern.sub(' ', str)
