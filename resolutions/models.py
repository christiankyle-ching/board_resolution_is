from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

from board_resolution_is import abstract_models

_User = get_user_model()


class Certificate(abstract_models.NoDeleteModel):
    added_by = models.ForeignKey(_User, null=True, on_delete=models.SET_NULL)
    added_date = models.DateTimeField(null=False, default=timezone.now)

    date_approved = models.DateField(blank=False, null=False)

    class Meta:
        ordering = ['-added_date']

    @property
    def resolutions(self):
        return Resolution.objects.filter(certificate=self)

    @property
    def images(self):
        return CertificateImage.objects.filter(certificate=self)


class Resolution(abstract_models.NoDeleteModel):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)

    number = models.CharField(max_length=50, blank=False, null=False)
    title = models.TextField(blank=False, null=False)

    class Meta:
        ordering = ['-pk']


class CertificateImage(abstract_models.NoDeleteModel):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)

    image = models.ImageField(upload_to="certificates/")
