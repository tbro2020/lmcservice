from django.shortcuts import get_object_or_404
from celery import shared_task

from wallet.models import Transaction
from service.models import Company


@shared_task
def solde(pk):
    if pk is None: return
    balance = Transaction.objects.filter(company_id=pk).balance()
    obj = get_object_or_404(Company, id=pk)
    obj.balance = balance
    obj.save()
