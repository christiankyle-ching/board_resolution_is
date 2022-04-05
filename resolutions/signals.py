from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from resolutions.models import Certificate, Resolution


@receiver(post_save, sender=Certificate)
def certificate_delete_resolutions_images(sender, instance, **kwargs):
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
            if remaining_res <= 0:
                instance.certificate.delete()
