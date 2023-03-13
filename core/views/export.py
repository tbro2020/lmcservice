from django.apps import apps

from django.shortcuts import HttpResponse
from django.views import View


class Export(View):
    def get(self, request, app, model):
        model = apps.get_model(app, model)
        qs = model.objects.filter(**request.GET.dict())
        # prepare the queryset to be export through excel as async request
        return HttpResponse("Export")
