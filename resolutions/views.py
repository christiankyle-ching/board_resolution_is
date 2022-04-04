from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

from resolutions.models import Certificate, CertificateImage, Resolution
from resolutions.utils import compress_image

RESOLUTION_PER_PAGE = 10


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        res = Resolution.objects.all()[:RESOLUTION_PER_PAGE]

        return render(request, 'resolutions/index.html', {
            'resolutions': res,
        })


class CertificateCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'resolutions/certificate_form.html', {})

    def post(self, request):
        date_approved = request.POST.get('date_approved')
        res_nums = request.POST.getlist('resolution_numbers')
        res_titles = request.POST.getlist('resolution_titles')

        cert = Certificate(date_approved=date_approved)
        cert.added_by = request.user

        cert_images = []
        resolutions = []

        for num, title in zip(res_nums, res_titles):
            res = Resolution(number=num, title=title, certificate=cert)
            resolutions.append(res)

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

        return render(request, 'resolutions/certificate_form.html', {})
