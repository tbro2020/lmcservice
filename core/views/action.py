from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from django.views import View
from django.apps import apps

from django.db.models.signals import post_save
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from service.models import *


class Action(LoginRequiredMixin, PermissionRequiredMixin, View):

    def get_permission_required(self):
        data = self.kwargs
        return f"{data.get('app')}.change_{data.get('model')}",

    def post(self, request, app, model):
        model = apps.get_model(app, model)
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        qs = model.objects.filter(**request.GET.dict())
        qs.update(**data)
        if qs.exists():
            post_save.send(model, instance=qs.last(), created=False)
        messages.success(request, "Action updated successfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
