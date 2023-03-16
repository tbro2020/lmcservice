from django.apps import apps

from django.shortcuts import HttpResponse
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class Export(LoginRequiredMixin, PermissionRequiredMixin, View):

    def get_permission_required(self):
        data = self.kwargs
        return f"{data.get('app')}.view_{data.get('model')}",

    def get(self, request, app, model):
        model = apps.get_model(app, model)
        qs = model.objects.filter(**request.GET.dict())
        # prepare the queryset to be export through excel as async request
        return HttpResponse("Export")
