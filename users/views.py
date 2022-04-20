from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View, generic
from django.contrib.auth.mixins import LoginRequiredMixin
from board_resolution_is.utils import get_form_errors
from resolutions.utils import compress_image
from django.contrib import messages

from os import linesep

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

            messages.success(request, 'Successfully updated profile.')
        elif 'update_avatar' in request.POST:
            avatar = request.FILES.get('avatar', '')
            if avatar != '':
                request.user.profile.avatar = compress_image(
                    avatar, max_px=512, force_jpeg=False)
                request.user.profile.save()

                messages.success(request, 'Successfully updated avatar.')
        elif 'remove_avatar' in request.POST:
            request.user.profile.avatar = None
            request.user.profile.save()

            messages.error(request, 'Removed avatar.')

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

            messages.success(request, 'Successfully changed password.')

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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            can_export = form.cleaned_data['can_export']
            # role = form.cleaned_data['role']

            _User.objects.create_user(username,
                                      email,
                                      password,
                                      # role=role
                                      can_export=can_export,
                                      )

            messages.success(
                request, f'Successfully created user: {username}.')

            return redirect(reverse('users:admin:manage'))

        return render(request, 'users/admin/user_create.html', {
            'form': form
        })


class AdminUserChangePasswordView(LoginRequiredMixin, HasAdminPermission, View):
    def get(self, request, pk):
        user = get_object_or_404(_User, pk=pk)

        return render(request, 'users/admin/user_change_password.html', {'selected_user': user, 'errors': []})

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

            messages.success(
                request, f'Successfully changed password for user: {user.username}.')

            return redirect(reverse('users:admin:manage'))
        else:
            messages.error(
                request, f'Errors found:{linesep}{linesep.join(errors)}')

        return render(request, 'users/admin/user_change_password.html', {'selected_user': user, 'errors': errors})


class AdminUserDeleteView(LoginRequiredMixin, HasAdminPermission, generic.DeleteView):
    model = _User
    template_name = 'users/admin/user_delete.html'
    success_url = reverse_lazy('users:admin:manage')
    context_object_name = 'selected_user'

    def get_success_url(self):
        messages.error(
            self.request, f"Deleted user: {self.get_object().username}.")

        return super().get_success_url()


class AdminUserEditView(LoginRequiredMixin, HasAdminPermission, generic.UpdateView):
    model = _User
    fields = ['email', 'can_export']
    template_name = 'users/admin/user_edit.html'
    context_object_name = 'selected_user'
    success_url = reverse_lazy('users:admin:manage')

    def get_success_url(self):
        messages.success(
            self.request, f"Successfully edited user: {self.get_object().username}.")

        return super().get_success_url()

# endregion
