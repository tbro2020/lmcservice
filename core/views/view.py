from django.contrib import messages
from django.apps import apps

from django.forms import modelform_factory, inlineformset_factory
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views import View

from core.utils import modelform_factory_data
from django.forms.fields import TypedChoiceField

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class Overview(LoginRequiredMixin, PermissionRequiredMixin, View):
    def get_permission_required(self):
        data = self.kwargs
        return f"{data.get('app')}.view_{data.get('model')}",

    def get(self, request, app, model, pk):
        model = apps.get_model(app, model)
        obj = get_object_or_404(model, pk=pk)

        if hasattr(model, "inline_model_form"):
            inline = getattr(model, "inline_model_form", {})
            _model = apps.get_model(inline.get("app_label"), inline.get("model_name"))
            related_fields = [field.name for field in _model._meta.get_fields()
                              if field.get_internal_type() == 'ForeignKey']
            # print(related_fields)
            qs = _model.objects.filter(**{model._meta.model_name: obj})
        return render(request, f"core/view.html", locals())
