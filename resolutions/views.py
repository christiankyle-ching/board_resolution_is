from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.utils import dateparse

from resolutions.models import Certificate, CertificateImage, Resolution
from resolutions.utils import compress_image

RESOLUTION_PER_PAGE = 10


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        res = Resolution.objects.all()[:RESOLUTION_PER_PAGE]

        return render(request, 'resolutions/index.html', {
            'resolutions': res,
        })


class CertificateFormView(LoginRequiredMixin, View):
    def get(self, request, res_pk=None):
        cert = None
        if res_pk is not None:
            cert = get_object_or_404(Resolution, pk=res_pk).certificate

        return render(request, 'resolutions/certificate_form.html', {
            'certificate': cert
        })

    def post(self, request, res_pk=None):
        # Get Form Values
        date_approved = request.POST.get('date_approved')
        res_nums = request.POST.getlist('resolution_numbers')
        res_titles = request.POST.getlist('resolution_titles')

        # Get existing cert, else create a new one
        cert = None
        if res_pk is not None:
            cert = get_object_or_404(Resolution, pk=res_pk).certificate
        else:
            cert = Certificate()
            cert.added_by = request.user

        # Update other fields
        cert.date_approved = dateparse.parse_date(date_approved)

        cert_images = []
        resolutions = []

        # Add New Resolutions
        for num, title in zip(res_nums, res_titles):
            num_stripped = num.strip()
            title_stripped = title.strip()
            if num_stripped != "" and title_stripped != "":
                res = Resolution(number=num_stripped,
                                 title=title_stripped, certificate=cert)
                resolutions.append(res)

        # Add New Files
        for f in request.FILES.getlist('images'):
            cert_image = CertificateImage(
                image=compress_image(f), certificate=cert)
            cert_images.append(cert_image)

        with transaction.atomic():
            cert.save()
            for r in resolutions:
                r.save()
            for ci in cert_images:
                ci.save()

        if res_pk is None:
            return redirect('resolutions:detail', res_pk=cert.resolutions[0].pk)

        return render(request, 'resolutions/certificate_form.html', {
            'certificate': cert,
        })


class CertificateDetailView(LoginRequiredMixin, View):
    def get(self, request, res_pk):
        cert = get_object_or_404(Resolution, pk=res_pk).certificate

        return render(request, 'resolutions/certificate_detail.html', {
            'certificate': cert,
        })
