from django.contrib.auth.mixins import UserPassesTestMixin


class HasAdminPermission(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_admin_permission


class HasExportPermission(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_export_permission


class HasStaffPermission(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_staff_permission
