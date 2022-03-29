from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django.conf import settings
from .models import ROLE_ADMIN, Profile


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def set_role(sender, instance, *args, **kwargs):
    # If user is superuser, make admin
    if instance.is_superuser:
        instance.role = ROLE_ADMIN


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    # if post request is creation,
    if created:
        # then create new Profile with user object of profile set to instance of User
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, created, **kwargs):
    # update the instance(User).profile by User.save()
    instance.profile.save()
