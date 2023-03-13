from django.contrib import messages
from django.apps import apps

from django.forms import modelform_factory, inlineformset_factory
from django.shortcuts import render, reverse, redirect
from django.views import View

from core.utils import modelform_factory_data


class Create(View):
    def get(self, request, app, model):
        model = apps.get_model(app, model)

        data = modelform_factory_data(model)
        form = modelform_factory(model, **data)

        if hasattr(model, "inline_model_form"):
            inline = getattr(model, "inline_model_form")
            _model = apps.get_model(app_label=inline.get("app_label"), model_name=inline.get("model_name"))
            _fields = _model.form_fields if hasattr(_model, "form_fields") else "__all__"
            inlineformset = inlineformset_factory(model, _model, form=modelform_factory(_model, fields=_fields), extra=1)
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
            inlineformset = inlineformset_factory(model, _model, form=modelform_factory(_model, fields=_fields),
                                                  extra=1)(request.POST)

        if not form.is_valid() or (inlineformset and not inlineformset.is_valid()):
            return render(request, f"core/create.html", locals())

        obj = form.save(commit=False)

        if hasattr(obj, "created_by"): obj.created_by = request.user
        if hasattr(obj, "company"): obj.company = request.user.company
        obj.save()

        if hasattr(model, "inline_model_form"):
            inlines = inlineformset.save(commit=False)
            for inline in inlines:
                if not hasattr(inline, inlineformset.fk.name): continue
                setattr(inline, inlineformset.fk.name, obj)
                inline.save()

        messages.success(request, f"{model._meta.verbose_name} created successfully")
        return redirect(
            reverse('core:edit', kwargs={"app": app, "model": model._meta.model_name, "pk": form.instance.id}))
