from django.apps import apps
from django.views import View
from django.db.models import Count, Sum
from django.shortcuts import render, get_object_or_404


# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.mixins import PermissionRequiredMixin


class Document(View):
    def get_permission_required(self):
        data = self.kwargs
        return f"{data.get('app')}.view_{data.get('model')}",

    def get(self, request, app, model, template, output="pdf"):
        model = apps.get_model(app, model)
        obj = get_object_or_404(model, **request.GET.dict())
        if hasattr(model, "inline_model_form"):
            data = getattr(model, "inline_model_form", {})
            _model = apps.get_model(app_label=data.get("app_label"), model_name=data.get("model_name"))
            qs = _model.objects.filter(**{model._meta.model_name: obj.id})
            if data.get("model_name") == "Product":
                qs = qs.values('product_type__name', 'product_type__fees', 'penalty').annotate(count=Sum('quantity'))
                print(qs)
        return render(request, f"document/{template}.html", locals())
