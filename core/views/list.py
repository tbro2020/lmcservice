from functools import reduce
import operator

from django.db.models import Q, Sum
from django.apps import apps

from django.shortcuts import render
from django.views import View

from core.paginator import Paginator
from core.filter import filterset_factory
from django.core.exceptions import FieldDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class List(LoginRequiredMixin, PermissionRequiredMixin, View):

    def get_permission_required(self):
        data = self.kwargs
        return f"{data.get('app')}.view_{data.get('model')}",

    def get(self, request, app, model):
        query = request.GET.dict()
        model = apps.get_model(app, model)
        field_names = [field.name for field in model._meta.get_fields()]
        query = {key: value for key, value in query.items() if key in field_names and value}

        # fields = [field for field in model._meta.fields if field.name in model.list_display_fields] if \
        #    hasattr(model, "list_display_fields") else \
        #    [field for field in model._meta.fields if field.get_internal_type() == 'CharField' or field.name == 'id']

        fields = model.list_display_fields if hasattr(model, "list_display_fields") else \
                 [field.name for field in model._meta.fields if field.get_internal_type() == 'CharField' or field.name == 'id']

        # apply filter according to the office or user limitation info to view
        qs = model.objects.values(*[field for field in fields]).filter(**query)
        if not request.user.is_superuser and request.user.office is not None and request.user.is_staff:
            _data = request.user.office.limitation.get("field", {}).get(model._meta.model_name, {})
            _data = {key: value for key, value in _data.items() if value}
            qs = qs.filter(**_data)

        try:
            if request.user.company and model._meta.get_field('company'):
                qs = qs.filter(company=request.user.company)
        except FieldDoesNotExist:
            print("field company not in model")

        if "q" in request.GET.dict():
            value = request.GET.dict().get("q", None)
            q = [Q(**{f"{field}__icontains": value}) for field in fields]
            qs = qs.filter(reduce(operator.or_, q))

        if hasattr(model, "filter_fields"):
            filter = filterset_factory(model, getattr(model, "filter_fields", []))(request.GET, queryset=qs)
            qs = filter.qs

        if model._meta.model_name.lower() == 'operation' and (request.user.is_superuser or request.user.has_perm('core.view_operation')):
            total_cost = qs.filter(cost__isnull=False).aggregate(total_cost=Sum('cost')).get('total_cost', 0)

        qs = qs.order_by("-id")
        qs = Paginator(qs, 30).page(request.GET.get('page', 1))
        return render(request, f"core/list.html", locals())
