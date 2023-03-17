import pdfkit
from django.apps import apps

from django.shortcuts import render, get_object_or_404, HttpResponse
from django.template.loader import get_template
from django.views import View

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class Document(LoginRequiredMixin, PermissionRequiredMixin, View):

    def get_permission_required(self):
        data = self.kwargs
        return f"{data.get('app')}.view_{data.get('model')}",

    def get(self, request, app, model, template, output="pdf"):
        model = apps.get_model(app, model)
        obj = get_object_or_404(model, **request.GET.dict())
        if hasattr(model, "inline_model_form"):
            data = getattr(model, "inline_model_form", {})
            qs = apps.get_model(app_label=data.get("app_label"), model_name=data.get("model_name")) \
                .objects.filter(**{model._meta.model_name: obj.id})
        # if output == "html":
        #    return render(request, f"document/{template}.html", locals())

        # template = get_template(f"document/{template}.html")
        # html = template.render(locals())

        # pdf = pdfkit.from_string(html, False, options={"page-size": "a4",
        #                                               'encoding': "UTF-8", 'no-outline': None,
        #                                                "enable-local-file-access": False},
        #                          configuration=settings.PDFKIT_CONFIG)
        # response = HttpResponse(pdf, content_type='application/pdf')

        # response['Content-Disposition'] = f'filename="{template}-#{obj.id}.pdf"'
        # return response
        return render(request, f"document/{template}.html", locals())
