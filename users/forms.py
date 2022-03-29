from django import forms
from django.contrib.auth import get_user_model

from users.models import ROLE_CHOICES, Profile

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

_User = get_user_model()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
        ]


class UserChangePasswordForm(forms.Form):
    old_password = forms.CharField(required=True, widget=forms.PasswordInput)
    new_password = forms.CharField(required=True, widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(
        required=True, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        uid = kwargs.pop('user_id', None)
        self.user = _User.objects.get(pk=uid)
        super(UserChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        new_password = self.cleaned_data['new_password']
        confirm_new_password = self.cleaned_data['confirm_new_password']

        if not self.user.check_password(self.cleaned_data['old_password']):
            raise ValidationError(
                _('Your old password is incorrect.'), code='old_password_incorrect')

        if new_password != confirm_new_password:
            raise ValidationError(
                _('New Password does not match.'), code='password_does_not_match')

        return super().clean()


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = _User
        fields = [
            'username',
            'email',
            'password',
            'role',
        ]
