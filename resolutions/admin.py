from django.contrib import admin

from resolutions.models import Certificate, CertificateImage, Resolution

# Register your models here.
admin.site.register(Resolution)
admin.site.register(Certificate)
admin.site.register(CertificateImage)
