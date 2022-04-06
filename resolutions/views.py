from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.utils import dateparse
from django.views import generic
from django.urls import reverse_lazy, reverse

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
    def get(self, request, pk=None):
        cert = None
        if pk is not None:
            cert = get_object_or_404(Certificate, pk=pk)

        return render(request, 'resolutions/certificate_form.html', {
            'certificate': cert
        })

    def post(self, request, pk=None):
        try:
            # Get Form Values
            date_approved = request.POST.get('date_approved')
            res_nums = request.POST.getlist('resolution_numbers')
            res_titles = request.POST.getlist('resolution_titles')

            # Get existing cert, else create a new one
            cert = None
            if pk is not None:
                cert = get_object_or_404(Certificate, pk=pk)
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
                    image=compress_image(f, image_format='PNG'), certificate=cert)
                cert_images.append(cert_image)

            with transaction.atomic():
                cert.save()
                for r in resolutions:
                    r.save()
                for ci in cert_images:
                    ci.save()

            return redirect('resolutions:cert_detail', pk=cert.pk)
        except Exception as e:
            print(e)
            return render(request, 'resolutions/certificate_form.html', {
                'certificate': cert,
            })


class CertificateDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            cert = Certificate.objects.get(pk=pk)
        except:
            return redirect('resolutions:index')

        return render(request, 'resolutions/certificate_detail.html', {
            'certificate': cert,
        })


class CertificateDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Certificate
    template_name = "resolutions/certificate_delete.html"
    success_url = reverse_lazy("resolutions:index")


# -------------------- Resolution Views --------------------
class ResolutionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Resolution
    template_name = "resolutions/resolution_delete.html"

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_last_resolution'] = self.get_object(
        ).certificate.resolutions.count() <= 1
        return context


class ResolutionEditView(LoginRequiredMixin, generic.UpdateView):
    model = Resolution
    template_name = 'resolutions/resolution_edit.html'
    fields = ['number', 'title']

    def get_success_url(self):
        return self.get_object().get_absolute_url()

# -------------------- Image Views --------------------


class CertificateImageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = CertificateImage
    template_name = "resolutions/certificate_image_delete.html"
    context_object_name = 'certificate_image'

    def get_success_url(self):
        return self.get_object().get_absolute_url()
