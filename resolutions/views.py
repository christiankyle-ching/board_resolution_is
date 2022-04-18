from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.utils import dateparse
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.db.models.query import Q
from django.core.paginator import Paginator
from django.http import FileResponse

from resolutions.forms import ResolutionSearchForm
from resolutions.models import Certificate, CertificateImage, Resolution
from resolutions.utils import PDFWithImageAndLabel, compress_image
from users.mixins import HasAdminPermission

RESOLUTION_PER_PAGE = 10


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        res = Resolution.objects.all()

        res_paginator = Paginator(res, RESOLUTION_PER_PAGE)
        page = request.GET.get('page')
        res_page_obj = res_paginator.get_page(page)

        search_form = ResolutionSearchForm()

        return render(request, 'resolutions/index.html', {
            'resolutions': res_page_obj,
            'search_form': search_form,
        })

    def post(self, request):
        res = Resolution.objects.all()

        search_form = ResolutionSearchForm(request.POST)
        has_searched = 'search' in request.POST and search_form.has_changed()

        if has_searched and search_form.is_valid():
            res = Resolution.objects.filter(
                (
                    Q(title__icontains=search_form.cleaned_data['title']) &
                    Q(number__icontains=search_form.cleaned_data['number'])
                )
            )

            if search_form.cleaned_data['date_approved'] is not None:
                res = res.filter(
                    certificate__date_approved=search_form.cleaned_data['date_approved'])
        else:

            return redirect('resolutions:index')

        return render(request, 'resolutions/index.html', {
            'resolutions': res,
            'search_form': search_form,
            'has_searched': has_searched,
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
            is_minutes_of_meeting = request.POST.get(
                'is_minutes_of_meeting') is not None
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
            cert.is_minutes_of_meeting = is_minutes_of_meeting

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


class CertificateExportView(LoginRequiredMixin, HasAdminPermission, View):
    def get(self, request, pk):
        cert = get_object_or_404(Certificate, pk=pk)

        res_numbers = []
        for r in cert.resolutions:
            res_numbers.append(r.number)

        # Generate PDF
        pdf = PDFWithImageAndLabel(
            orientation="P", unit="in", format=(8.5, 13))
        pdf.set_margin(0)
        pdf.oversized_images = "DOWNSCALE"
        pdf.allow_images_transparency = False  # To prevent black background on print
        pdf.set_auto_page_break(False)

        for img in cert.images:
            pdf.add_page()
            pdf.add_image(img.image.path)

            # pdf.add_lines_of_text([
            #     "Resolutions Included:",
            #     *map(
            #         lambda r: f"Resolution No. {r.number} - {r.title}",
            #         cert.resolutions),
            #     "",
            #     "Date Approved:",
            #     cert.date_approved.strftime('%B %d, %Y'),
            # ])

        byte_str = pdf.output(dest='S')
        stream = BytesIO(byte_str)

        return FileResponse(stream, as_attachment=True, filename=f'resolution_{"_".join(map(lambda r: r.number, cert.resolutions))}_export.PDF')

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
