from django.contrib import messages
from django.apps import apps

from django.forms import modelform_factory, inlineformset_factory
from django.shortcuts import render, reverse, redirect
from django.views import View

from core.utils import modelform_factory_data


class CreateCompany(View):
    def get(self, request):
        model = apps.get_model("service", "company")
        data = modelform_factory_data(model)
        form = modelform_factory(model, **data)
        return render(request, f"registration/create_company.html", locals())

    def post(self, request, app, model):
        model = apps.get_model("service", "company")
        data = modelform_factory_data(model)
        form = modelform_factory(model, **data)(request.POST, request.FILES)

        if not form.is_valid():
            return render(request, f"registration/create_company.html", locals())
        form.save()

        messages.success(request, f"{model._meta.verbose_name} created successfully")
        messages.success(request, "We are reviewing your registration, and will mail your with a confirmation")
        return redirect(reverse('login'))
