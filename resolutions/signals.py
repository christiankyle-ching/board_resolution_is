from django.db.models.signals import post_delete
from django.dispatch import receiver

from resolutions.models import Resolution


@receiver(post_delete, sender=Resolution)
def delete_certificate(sender, instance, **kwargs):
    if instance.certificate.resolutions.length <= 0:
        instance.certificate.delete()
