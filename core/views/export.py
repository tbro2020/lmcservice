from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from django.views import View
from django.apps import apps

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from service import tasks
from urllib.parse import urlencode


class Export(LoginRequiredMixin, PermissionRequiredMixin, View):

    def get_permission_required(self):
        data = self.kwargs
        return f"{data.get('app')}.view_{data.get('model')}",

    def get(self, request, app, model):
        query = request.GET.dict()

        model = apps.get_model(app, model)
        fields = [field.name for field in model._meta.get_fields()]
        query = {key: value for key, value in query.items() if key in fields and value}

        if not request.user.is_superuser and request.user.office is not None and request.user.is_staff:
            filters = request.user.office.limitation.get("field", {}).get(model._meta.model_name, {})
            filters = {key: value for key, value in filters.items() if value}
            query = filters | query
        if request.user.company: query["company_id"] = request.user.company_id
        tasks.report.delay(app, model._meta.model_name, query, request.user.email)
        messages.success(request, f"We will shortly send the report to <b>{request.user.email}</b>")
        return HttpResponseRedirect(f"{request.META.get('HTTP_REFERER', '/')}?{urlencode({key: value for key, value in request.GET.dict().items() if value})}")
