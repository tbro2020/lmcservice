from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from django.apps import apps

from rest_framework.authentication import TokenAuthentication


class OperationAPIView(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        data = dict(request.data)
        if "next" in data: del data["next"]
        CheckPoint = apps.get_model("service", "checkpoint")
        if "location" not in request.data or not request.user.is_staff: raise Http404()

        data.update({"operation_id": data.get("operation", None), "product_id": data.get("product", None)})
        [data.pop(key) for key in ["operation", "product", "device_info"] if key in data.keys()]
        checkpoint, created = CheckPoint.objects.get_or_create(**data)

        if not created:
            return Response(
                {"id": checkpoint.id, "url": checkpoint.url(request), "status": checkpoint.operation.status})

        checkpoint.user = request.user
        checkpoint.location = request.data["location"]
        checkpoint.save()

        return Response({"id": checkpoint.id, "url": checkpoint.url(request), "status": checkpoint.operation.status})
