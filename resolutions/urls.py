from django.urls import path

from . import views

app_name = "resolutions"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('create/', views.CertificateFormView.as_view(), name='create'),
    path('<int:res_pk>/edit/', views.CertificateFormView.as_view(), name='edit'),
    path('<int:res_pk>/', views.CertificateDetailView.as_view(), name='detail'),
]
