from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from django.views import View
from django.apps import apps

from django.db.models.signals import post_save
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import PermissionRequiredMixin


class Action(LoginRequiredMixin, PermissionRequiredMixin, View):
    def get_permission_required(self):
        data = self.kwargs
        return f"{data.get('app')}.change_{data.get('model')}",

    def post(self, request, app, model, verbose):
        model = apps.get_model(app, model)
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        qs = model.objects.filter(**request.GET.dict())
        if not qs.exists():
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        actions = [action for action in model.change_actions
                   if action.get("prerequisite") and action.get("verbose_name") == verbose]
        actions = actions[0] if len(actions) == 1 else {}

        if actions.get("prerequisite", False):
            prerequisite = actions.get("prerequisite")
            obj = qs.last()
            if not eval(prerequisite.get("condition")):
                messages.error(request, prerequisite.get("message", {}).get("error", "We fail this action"))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            action = eval(prerequisite.get("action", "False"))
            if action: messages.success(request, prerequisite.get("message", {}).get("success", "Action success"))

        qs.update(**data)
        post_save.send(model, instance=qs.last(), created=False)
        messages.success(request, "Action updated successfully")

        obj = qs.last()
        LogEntry.objects.log_action(user_id=request.user.id, content_type_id=ContentType.objects.get_for_model(obj).pk,
                                    object_id=obj.id, object_repr=f"Modification de {obj}",
                                    action_flag=CHANGE, change_message=str(data))

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
