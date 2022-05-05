from django.urls import path

from . import views

app_name = "resolutions"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('create/', views.CertificateFormView.as_view(), name='create'),

    # Certificate Views
    path('certificate/<int:pk>/',
         views.CertificateDetailView.as_view(), name='cert_detail'),
    path('certificate/<int:pk>/edit/',
         views.CertificateFormView.as_view(), name='cert_edit'),
    path('certificate/<int:pk>/delete/',
         views.CertificateDeleteView.as_view(), name='cert_delete'),

    # Resolution Views
    path('resolution/<int:pk>/edit/',
         views.ResolutionEditView.as_view(), name='res_edit'),
    path('resolution/<int:pk>/delete/',
         views.ResolutionDeleteView.as_view(), name='res_delete'),

    # Certificate Image Views
    path('certificate-image/<int:pk>/delete/',
         views.CertificateImageDeleteView.as_view(), name='cert_image_delete'),

    # Export Views
    path('certificate/<int:pk>/export',
         views.CertificateExportView.as_view(), name="cert_export"),

    path('db_dump/resolutions/import/',
         views.ResolutionDumpImportView.as_view(), name="db_res_import"),
    path('db_dump/resolutions/export/',
         views.ResolutionDumpExportView.as_view(), name="db_res_export"),

    # History
    path('history/', views.HistoryView.as_view(), name='history'),
]
