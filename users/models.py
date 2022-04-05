from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.templatetags.static import static

# AVOID CHANGING THESE
ROLE_ADMIN = 0
ROLE_STAFF = 1

ROLE_CHOICES = (
    (ROLE_ADMIN, 'Admin'),
    (ROLE_STAFF, 'Staff'),
)


class ActiveUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    role = models.PositiveSmallIntegerField(
        null=False, blank=False, default=ROLE_STAFF, choices=ROLE_CHOICES)
    can_export = models.BooleanField(default=False)

    objects = ActiveUserManager()
    all_objects = UserManager()

    def delete(self):
        self.deactivate()

    def deactivate(self):
        self.is_active = False
        self.save()

    def reactivate(self):
        self.is_active = True
        self.save()

    @property
    def role_name(self):
        return dict(ROLE_CHOICES)[self.role]

    @property
    def has_admin_permission(self):
        return self.role in [ROLE_ADMIN]

    @property
    def has_staff_permission(self):
        return self.role in [ROLE_ADMIN, ROLE_STAFF]

    @property
    def has_export_permissions(self):
        return self.has_admin_permission or self.can_export


class Profile(models.Model):
    def avatar_path(instance, filename):
        return f"users/user-{instance.user.id}/{filename}"

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)

    avatar = models.ImageField(upload_to=avatar_path)
    first_name = models.CharField(blank=True, max_length=50)
    last_name = models.CharField(blank=True, max_length=50)

    @property
    def full_name(self):
        if self.first_name == '' and self.last_name == '':
            return 'Unnamed'

        return f"{self.first_name} {self.last_name}"

    @property
    def avatar_url(self):

        print(self.avatar)
        if self.avatar:
            return self.avatar.url

        return static('users/img/user.png')
