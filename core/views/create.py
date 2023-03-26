from django.contrib import messages
from django.apps import apps

from django.forms import modelform_factory, inlineformset_factory
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, reverse, redirect
from django.views import View

from core.utils import modelform_factory_data

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.admin.utils import construct_change_message


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
        form = modelform_factory(model, **data)(request.POST, request.FILES)

        inlineformset = None
        if hasattr(model, "inline_model_form"):
            inline = getattr(model, "inline_model_form")
            _model = apps.get_model(app_label=inline.get("app_label"), model_name=inline.get("model_name"))
            _fields = _model.form_fields if hasattr(_model, "form_fields") else "__all__"
            inlineformset = inlineformset_factory(model, _model, form=modelform_factory(_model, fields=_fields))
            inlineformset = inlineformset(request.POST, request.FILES)

        if not form.is_valid() or (inlineformset and not inlineformset.is_valid()):
            return render(request, f"core/create.html", locals())

        obj = form.save(commit=False)
        if isinstance(obj, apps.get_model("service", "operation")):
            obj.created_by = request.user
            obj.company = request.user.company
        if isinstance(obj, apps.get_model("core", "user")): obj.company = request.user.company
        obj.save()

        # Inherent permission
        if isinstance(obj, apps.get_model("core", "user")): obj.groups.add(*list(request.user.groups.all()))

        if hasattr(model, "inline_model_form"):
            inlines = inlineformset.save(commit=False)
            for inline in inlines:
                if not hasattr(inline, inlineformset.fk.name): continue
                setattr(inline, inlineformset.fk.name, obj)
                inline.save()
            inlineformset.save_m2m()

        messages.success(request, f"{model._meta.verbose_name} created successfully")
        message = construct_change_message(form, inlineformset, True)
        LogEntry.objects.log_action(user_id=request.user.id, content_type_id=ContentType.objects.get_for_model(obj).pk,
                                    object_id=obj.id, object_repr=f"Creation de {obj}",
                                    action_flag=ADDITION, change_message=str(message))
        return redirect(reverse('core:edit', kwargs={"app": app, "model": model._meta.model_name, "pk": form.instance.id}))
