from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from django.views import View
from django.apps import apps


class Action(View):
    def post(self, request, app, model):
        model = apps.get_model(app, model)
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        model.objects.filter(**request.GET.dict()).update(**data)

        messages.success(request, "Action updated successfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
