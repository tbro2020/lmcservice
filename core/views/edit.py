from django.contrib import messages
from django.apps import apps

from django.forms import modelform_factory, inlineformset_factory
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views import View

from core.utils import modelform_factory_data
from django.forms.fields import TypedChoiceField


def modelAndFields(request, model):
    inline = getattr(model, "inline_model_form")
    _model = apps.get_model(app_label=inline.get("app_label"), model_name=inline.get("model_name"))
    _fields = [field for field in _model.form_fields] if hasattr(model, "form_fields") else "__all__"

    if hasattr(_model, "extra") and "fields" in _model.extra:
        for field in _model.extra.get("fields"):
            if eval(field.get("condition")):
                _fields.append(field.get("name"))
    return _model, _fields


class Edit(View):
    def get(self, request, app, model, pk):
        model = apps.get_model(app, model)

        obj = get_object_or_404(model, pk=pk)
        data = modelform_factory_data(model)

        if hasattr(model, "extra") and "fields" in model.extra:
            for field in model.extra.get("fields"):
                if eval(field.get("condition")):
                    data["fields"].append(field.get("name"))

        form = modelform_factory(model, **data)(instance=obj)

        if request.user.is_staff and request.user.office \
                and request.user.office.limitation.get("value", {}).get(model._meta.model_name, False):
            for key, value in request.user.office.limitation.get("value", {}).get(model._meta.model_name, {}).items():
                if key not in form.fields: continue
                if not isinstance(form.fields[key], TypedChoiceField): continue
                form.fields[key].choices = [choice for choice in form.fields[key].choices if choice[0] in value]

        if hasattr(model, "inline_model_form"):
            inline = modelAndFields(request, model)
            inlineformset = inlineformset_factory(model, inline[0], form=modelform_factory(inline[0], fields=inline[1]),
                                                  extra=1, can_delete_extra=True)(instance=obj)

        return render(request, f"core/update.html", locals())

    def post(self, request, app, model, pk):
        model = apps.get_model(app, model)
        obj = get_object_or_404(model, pk=pk)

        data = modelform_factory_data(model)

        if hasattr(model, "extra") and "fields" in model.extra:
            for field in model.extra.get("fields"):
                if eval(field.get("condition")):
                    data["fields"].append(field.get("name"))

        form = modelform_factory(model, **data)(request.POST or None, instance=obj)

        if request.user.is_staff and request.user.office \
                and request.user.office.limitation.get("value", {}).get(model._meta.model_name, False):
            for key, value in request.user.office.limitation.get("value", {}).get(model._meta.model_name, {}).items():
                if key not in form.fields: continue
                if not isinstance(form.fields[key], TypedChoiceField): continue
                form.fields[key].choices = [choice for choice in form.fields[key].choices if choice[0] in value]

        if hasattr(model, "inline_model_form"):
            inline = modelAndFields(request, model)
            inlineformset = inlineformset_factory(model, inline[0], form=modelform_factory(inline[0], fields=inline[1]),
                                                  extra=1)(request.POST or None, request.FILES or None, instance=obj)

        if not form.is_valid() or (hasattr(locals(), "inlineformset") and not inlineformset.is_valid()):
            return render(request, f"core/update.html", locals())

        obj = form.save(commit=True)
        if hasattr(obj, "updated_by"): obj.updated_by = request.user

        obj.save()
        if hasattr(model, "inline_model_form"): inlineformset.save()
        messages.success(request, f"{model._meta.verbose_name} updated successfully")
        return redirect(reverse('core:edit', kwargs={"app": app, "model": model._meta.model_name, "pk": pk}))