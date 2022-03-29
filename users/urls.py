from django.urls import path, include, reverse_lazy
from django.conf import settings

from . import views
from django.contrib.auth import views as auth_views

app_name = "users"

admin_urlpatterns = ([
    path('manage/', views.AdminManageView.as_view(), name='manage'),
    path('create/', views.AdminUserCreateView.as_view(), name='user_create'),
    path('<int:pk>/delete/', views.AdminUserDeleteView.as_view(), name='user_delete'),
    path('<int:pk>/change_password/', views.AdminUserChangePasswordView.as_view(),
         name='user_change_password'),
], 'admin')

auth_urlpatterns = ([
    path('login/', auth_views.LoginView.as_view(template_name='users/auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/auth/login.html'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/auth/password_reset.html',
        email_template_name='users/auth/password_reset_email.html',
        html_email_template_name='users/auth/password_reset_email.html',
        success_url=reverse_lazy('users:auth:password_reset_done'),
        subject_template_name='users/auth/password_reset_subject.txt',
        extra_email_context={
            'site_name': settings.CLIENT_NAME,
        }),
        name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/auth/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/auth/password_reset_confirm.html',
        success_url=reverse_lazy('users:auth:password_reset_complete')),
        name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/auth/password_reset_complete.html'),
        name='password_reset_complete'),
], 'auth')

urlpatterns = [
    # Default Auth Views
    path('auth/', include(auth_urlpatterns)),

    # Profile Views
    path('profile_change_password/', views.UserChangePasswordView.as_view(),
         name='profile_change_password'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),

    # Admin Only
    path('admin/', include(admin_urlpatterns))
]
