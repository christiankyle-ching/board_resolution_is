from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

from board_resolution_is import abstract_models

_User = get_user_model()


class Certificate(abstract_models.NoDeleteModel):
    added_by = models.ForeignKey(_User, null=True, on_delete=models.SET_NULL)
    added_date = models.DateTimeField(null=False, default=timezone.now)

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
        # return f"Certificate approved at {self.date_approved.strftime('%B %d, %Y')}"

    def get_absolute_url(self):
        return reverse("resolutions:cert_detail", kwargs={'pk': self.pk})


class Resolution(abstract_models.NoDeleteModel):
    added_date = models.DateTimeField(null=False, default=timezone.now)

    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)

    number = models.CharField(max_length=50, blank=False, null=False)
    title = models.TextField(blank=False, null=False)

    class Meta:
        ordering = ['-added_date']

    def __str__(self):
        return f"Res. No. {self.number} - {self.title}"

    def get_absolute_url(self):
        return reverse("resolutions:cert_detail", kwargs={'pk': self.certificate.pk})


class CertificateImage(abstract_models.NoDeleteModel):
    def certificate_image_path(instance, filename):
        return f"certificates/cert-{instance.certificate.id}/{filename}"

    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)

    image = models.ImageField(upload_to=certificate_image_path)

    def __str__(self):
        return self.image.name

    class Meta:
        ordering = ['image']

    def get_absolute_url(self):
        return reverse('resolutions:cert_detail', kwargs={'pk': self.certificate.pk})
