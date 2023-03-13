from django.apps import apps

from django.shortcuts import render, reverse, redirect, get_object_or_404, HttpResponse
from django.views import View


class Delete(View):
    def get(self, request, app, model, pk):
        model = apps.get_model(app, model)

        obj = get_object_or_404(model, pk=pk)
        return render(request, f"core/delete.html", locals())

    def post(self, request, app, model, pk):
        model = apps.get_model(app, model)

        obj = get_object_or_404(model, pk=pk)
        obj.delete()
        return redirect(reverse('core:list', kwargs={"app": app, "model": model._meta.model_name, "page": 1}))
