from django.contrib import messages
from django.apps import apps

from django.forms import modelform_factory, inlineformset_factory
from django.shortcuts import render, reverse, redirect
from django.views import View

from core.utils import modelform_factory_data

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from core.models import User


class Create(LoginRequiredMixin, PermissionRequiredMixin, View):

    def get_permission_required(self):
        data = self.kwargs
        return f"{data.get('app')}.add_{data.get('model')}",

    def get(self, request, app, model):
        model = apps.get_model(app, model)

        data = modelform_factory_data(model)
        form = modelform_factory(model, **data)

        if hasattr(model, "inline_model_form"):
            inline = getattr(model, "inline_model_form")
            _model = apps.get_model(app_label=inline.get("app_label"), model_name=inline.get("model_name"))
            _fields = _model.form_fields if hasattr(_model, "form_fields") else "__all__"
            inlineformset = inlineformset_factory(model, _model, form=modelform_factory(_model, fields=_fields),
                                                  extra=1, can_delete=False)
        return render(request, f"core/create.html", locals())

    def post(self, request, app, model):
        model = apps.get_model(app, model)

        data = modelform_factory_data(model)
        form = modelform_factory(model, **data)(request.POST or None, request.FILES or None)

        inlineformset = None
        if hasattr(model, "inline_model_form"):
            inline = getattr(model, "inline_model_form")
            _model = apps.get_model(app_label=inline.get("app_label"), model_name=inline.get("model_name"))
            _fields = _model.form_fields if hasattr(_model, "form_fields") else "__all__"
            inlineformset = inlineformset_factory(model, _model, form=modelform_factory(_model, fields=_fields))
            inlineformset = inlineformset(request.POST)

        if not form.is_valid() or (inlineformset and not inlineformset.is_valid()):
            return render(request, f"core/create.html", locals())

        obj = form.save(commit=False)

        fields = [field.name for field in model._meta.fields]
        if "created_by" in fields: obj.created_by = request.user
        if "company" in fields: obj.company = request.user.company
        obj.save()

        # Inherent permission
        if isinstance(obj, User): obj.groups.add(*list(request.user.groups.all()))

        if hasattr(model, "inline_model_form"):
            inlines = inlineformset.save(commit=False)
            for inline in inlines:
                if not hasattr(inline, inlineformset.fk.name): continue
                setattr(inline, inlineformset.fk.name, obj)
                inline.save()

        messages.success(request, f"{model._meta.verbose_name} created successfully")
        return redirect(
            reverse('core:edit', kwargs={"app": app, "model": model._meta.model_name, "pk": form.instance.id}))
