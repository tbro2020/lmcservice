from django.shortcuts import get_object_or_404, render
from django.views import View
from django.apps import apps


class CheckPointATM(View):
    def get(self, request, checkpoint):
        CheckPoint = apps.get_model("service", "checkpoint")
        Product = apps.get_model("service", "product")

        checkpoint = get_object_or_404(CheckPoint, id=checkpoint)
        products = Product.objects.filter(operation=checkpoint.operation)
        if checkpoint.product: products = products.filter(id=checkpoint.product.id)
        return render(request, "checkpoint/atm.html", locals())
