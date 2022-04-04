from django.urls import path

from . import views

app_name = "resolutions"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.CertificateCreateView.as_view(), name='create'),
]
