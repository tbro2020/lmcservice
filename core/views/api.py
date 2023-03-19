from rest_framework.response import Response
from rest_framework.views import APIView
from django.views import View

from django.apps import apps
from django.http import Http404
from django.shortcuts import get_object_or_404, render


Operation = apps.get_model("service", "operation")
Product = apps.get_model("service", "product")
CheckPoint = apps.get_model("service", "checkpoint")

class OperationAPIView(APIView):
    def post(self, request):
        data = dict()
        data["operation"] = get_object_or_404(Operation, id=request.data["operation"])
        if "location" not in request.data or "device_info" not in request.data: raise Http404()

        if "product" in request.data:
            _data = {"operation": data["operation"], id: request.data.get("product")}
            data["product"] = get_object_or_404(Product, **_data)
        checkpoint, created = CheckPoint.objects.get_or_create(**data)

        if not created:
            return Response(
                {"id": checkpoint.id, "url": checkpoint.url(request), "status": checkpoint.operation.status})

        checkpoint.user = request.user
        checkpoint.location = request.data["location"]
        checkpoint.device_info = request.data["device_info"]
        checkpoint.save()

        return Response({"id": checkpoint.id, "url": checkpoint.url(request), "status": checkpoint.operation.status})


class CheckPointATM(View):
    def get(self, request, checkpoint):
        checkpoint = get_object_or_404(CheckPoint, id=checkpoint)
        products = Product.objects.filter(operation=checkpoint.operation)
        if checkpoint.product: products = products.filter(id=checkpoint.product.id)
        return render(request, "checkpoint/atm.html", locals())
