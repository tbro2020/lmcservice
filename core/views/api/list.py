from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from django.apps import apps

from rest_framework.authentication import TokenAuthentication
from rest_framework import serializers


class ListAPI(APIView):
    authentication_classes = (TokenAuthentication,)

    def get_permission_required(self):
        data = self.kwargs
        return f"{data.get('app')}.view_{data.get('model')}",

    def get(self, request, app, model):
        if not request.user.has_perm(self.get_permission_required()): Http404()
        print(request.user)
        model = apps.get_model(app, model)
        query = request.GET.dict()
        if "format" in query: del query["format"]
        query["user"] = request.user.id  # show only connected user information
        qs = model.objects.filter(**query)[:120]
        serializer = type(f'Serializer', (serializers.ModelSerializer,),
                          {'Meta': type('Meta', (object,), {'model': model, 'fields': '__all__', 'depth': 1})})
        return Response(serializer(qs, many=True).data)
