from django.shortcuts import render
from django.db.models import Count
from django.views import View
from service import models
from datetime import datetime


class Home(View):
    def get(self, request):
        qs = models.Operation.objects.filter(created__year=datetime.today().year)

        # case of staff
        if request.user.is_staff and request.user.office is not None:
            qs = qs.filter(**request.user.office.limitation.get("field", {}).get("operation", {}))

        # Case of forwarder user
        if request.user.company is not None: qs = qs.filter(company=request.user.company)
        data = {"pie": {"labels": [], "data": []}, "bar": {"labels": [], "data": {}}}

        status = qs.values("status").annotate(Count("status"))
        for pie in status:
            data["pie"]["labels"].append(pie.get("status"))
            data["pie"]["data"].append(pie.get("status__count"))

        bars = qs.values("status", "created__month").annotate(Count("status"))

        for bar in bars:
            data["bar"]["labels"].append(bar.get("created__month"))
            if bar.get("status") not in data["bar"]["data"]:
                data["bar"]["data"][bar.get("status")] = []
            data["bar"]["data"][bar.get("status")].append(bar.get("status__count"))

        data["bar"]["labels"] = [datetime.strptime(str(label), "%m").strftime("%B") for label in data["bar"]["labels"]]
        return render(request, "home.html", locals())
