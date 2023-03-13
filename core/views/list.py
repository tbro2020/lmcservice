from functools import reduce
import operator

from django.db.models import Q
from django.apps import apps

from django.shortcuts import render
from django.views import View

from core.paginator import Paginator
from django.core.exceptions import FieldDoesNotExist


class List(View):
    def get(self, request, app, model, page):
        model = apps.get_model(app, model)
        data = request.GET.dict()
        if "q" in data: del data["q"]

        fields = [field for field in model._meta.fields if field.name in model.list_display_fields] if \
            hasattr(model, "list_display_fields") else \
            [field for field in model._meta.fields if field.get_internal_type() == 'CharField' or field.name == 'id']

        # apply filter according to the office or user limitation info to view
        qs = model.objects.values(*[field.name for field in fields]).filter(**data)
        if not request.user.is_superuser and request.user.office is not None and request.user.is_staff:
            qs = qs.filter(**request.user.office.limitation.get("field", {}).get(model._meta.model_name, {}))

        try:
            if request.user.company and model._meta.get_field('company'):
                qs = qs.filter(company=request.user.company)
        except FieldDoesNotExist:
            print("field company not in model")

        if "q" in request.GET.dict():
            value = request.GET.dict().get("q", None)
            q = [Q(**{f"{field.name}__icontains": value}) for field in fields if
                 field.get_internal_type() == 'CharField']
            qs = qs.filter(reduce(operator.or_, q))
        qs = qs.order_by("-id")
        qs = Paginator(qs, 30).page(page)
        return render(request, f"core/list.html", locals())
