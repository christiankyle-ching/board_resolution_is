from django import forms
from django.contrib.auth import get_user_model, password_validation

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
        cleaned_data = super(UserChangePasswordForm, self).clean()

        old_password = cleaned_data.get('old_password', '')
        new_password = cleaned_data.get('new_password', '')
        confirm_new_password = cleaned_data.get('confirm_new_password', '')

        if not self.user.check_password(old_password):
            raise ValidationError(
                _('Your old password is incorrect.'), code='old_password_incorrect')

        if new_password != confirm_new_password:
            raise ValidationError(
                _('New Password does not match.'), code='password_does_not_match')

        password_validation.validate_password(new_password)

        return cleaned_data


class UserChangeEmailForm(forms.Form):
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    new_email = forms.EmailField(required=True)
    confirm_new_email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        uid = kwargs.pop('user_id', None)
        self.user = _User.objects.get(pk=uid)
        super(UserChangeEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(UserChangeEmailForm, self).clean()

        password = cleaned_data.get('password', '')
        new_email = cleaned_data.get('new_email', '')
        confirm_new_email = cleaned_data.get('confirm_new_email')

        if not self.user.check_password(password):
            raise ValidationError(
                _('Your password is incorrect.'), code='password_incorrect')

        if new_email != confirm_new_email:
            raise ValidationError(
                _('New Email does not match.'), code='password_does_not_match')

        if _User.objects.filter(email=new_email).exclude(pk=self.user.pk).exists():
            raise ValidationError(
                _('Email is already used by another user.'), code='email_not_unique')

        return cleaned_data


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = _User
        fields = [
            'username',
            'email',
            'password',
            # 'role',
            'can_export'
        ]

    def clean(self):
        cleaned_data = super(UserCreateForm, self).clean()

        email = cleaned_data['email']
        username = cleaned_data['username']

        email_exists = _User.all_objects.filter(email=email).exists()
        username_exists = _User.all_objects.filter(username=username).exists()

        errors = []

        if email_exists:
            errors.append(ValidationError(
                _('Email already exists "%(email)s".'), params={'email': email}))

        if username_exists:
            errors.append(ValidationError(
                _('Username already exists "%(username)s".'), params={'username': username}))

        if len(errors) > 0:
            raise ValidationError(errors)

        password_validation.validate_password(cleaned_data['password'])

        return cleaned_data


class AdminUserChangePasswordForm(forms.Form):
    new_password = forms.CharField(required=True, widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(
        required=True, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        uid = kwargs.pop('user_id', None)
        self.user = _User.objects.get(pk=uid)
        super(AdminUserChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(AdminUserChangePasswordForm, self).clean()

        new_password = cleaned_data.get('new_password', '')
        confirm_new_password = cleaned_data.get('confirm_new_password', '')

        if new_password != confirm_new_password:
            raise ValidationError(
                _('New Password does not match.'), code='password_does_not_match')

        password_validation.validate_password(new_password)

        return cleaned_data
