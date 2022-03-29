from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View, generic
from django.contrib.auth.mixins import LoginRequiredMixin
from board_resolution_is_v2.utils import get_form_errors

from users.mixins import HasAdminPermission

from .forms import UserChangePasswordForm, UserCreateForm, UserProfileForm

from django.contrib.auth import get_user_model

_User = get_user_model()


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile_form = UserProfileForm(instance=request.user.profile)

        return render(request, 'users/profile.html', {
            'profile_form': profile_form,
        })

    def post(self, request):
        profile_form = UserProfileForm(instance=request.user.profile)

        if 'update_profile' in request.POST:
            profile_form = UserProfileForm(
                request.POST, instance=request.user.profile)
            profile_form.save()
        elif 'update_avatar' in request.POST:
            avatar = request.FILES.get('avatar', '')
            if avatar != '':
                request.user.profile.avatar = avatar
                request.user.profile.save()
        elif 'remove_avatar' in request.POST:
            request.user.profile.avatar = None
            request.user.profile.save()

        return render(request, 'users/profile.html', {
            'profile_form': profile_form,
        })


class UserChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        password_form = UserChangePasswordForm(user_id=request.user.id)

        return render(request, 'users/change_password.html', {
            'password_form': password_form,
        })

    def post(self, request):
        password_form = UserChangePasswordForm(
            request.POST, user_id=request.user.id)

        if password_form.is_valid():
            request.user.set_password(
                password_form.cleaned_data['new_password'])

            request.user.save()

            return redirect(reverse('users:profile_change_password'))

        return render(request, 'users/change_password.html', {
            'password_form': password_form,
        })


# region ADMIN VIEWS


class AdminManageView(LoginRequiredMixin, HasAdminPermission, View):
    def get(self, request):
        users = _User.objects.all().exclude(id=request.user.id)

        return render(request, 'users/admin/users_manage.html', {
            'users': users
        })


class AdminUserCreateView(LoginRequiredMixin, HasAdminPermission, View):
    def get(self, request):
        form = UserCreateForm()

        return render(request, 'users/admin/user_create.html', {
            'form': form
        })

    def post(self, request):
        form = UserCreateForm(request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            role = request.POST.get('role')

            _User.objects.create_user(username, email, password, role=role)

            return redirect(reverse('users:admin:manage'))

        return render(request, 'users/admin/user_create.html', {
            'form': form
        })


class AdminUserChangePasswordView(LoginRequiredMixin, HasAdminPermission, View):
    def get(self, request, pk):
        user = get_object_or_404(_User, pk=pk)

        return render(request, 'users/admin/user_change_password.html', {'user': user, 'errors': []})

    def post(self, request, pk):
        user = get_object_or_404(_User, pk=pk)

        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        errors = get_form_errors([
            (password != '' and confirm_password !=
             '', 'Password cannot be empty.'),
            (password == confirm_password, 'Password does not match.')
        ])

        # If no errors, try change password
        if len(errors) <= 0:
            user.set_password(password)
            user.save()

            return redirect(reverse('users:admin:manage'))

        return render(request, 'users/admin/user_change_password.html', {'user': user, 'errors': errors})


class AdminUserDeleteView(LoginRequiredMixin, HasAdminPermission, generic.DeleteView):
    model = _User
    template_name = 'users/admin/user_delete.html'
    success_url = reverse_lazy('users:admin:manage')

# endregion
