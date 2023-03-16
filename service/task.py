from django.shortcuts import get_object_or_404
from celery import shared_task
from django.apps import apps


from lmcservice.mailer import Mailer
from service.models import *


@shared_task
def operation(pk):
    obj = get_object_or_404(Operation, id=pk)
    obj.cost = obj.total()
    obj.save()
    print(f"Cost {obj.id} updated")


@shared_task
def mailer(app, model, pk, template, subject, to):
    model = apps.get_model(app, model)
    context = model.objects \
        .values(*[field.name for field in model._meta.get_fields()]).filter(id=pk).first()
    Mailer(template, context, subject, to).send()


@shared_task
def report(app, model):
    model = apps.get_model(app, model)
    # apply filter & exclude
    return
