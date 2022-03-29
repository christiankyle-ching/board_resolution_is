from django.contrib.auth.mixins import UserPassesTestMixin

from users.models import ROLE_ADMIN, ROLE_STAFF


class HasAdminPermission(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role in [ROLE_ADMIN]


class CanExportPermission(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role in [ROLE_ADMIN] or self.request.user.can_export


class HasStaffPermission(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role in [ROLE_ADMIN, ROLE_STAFF]
