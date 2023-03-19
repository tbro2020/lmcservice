from django.db.models import QuerySet
from django.db.models import Sum


class TransactionQuerySet(QuerySet):
    def balance(self):
        value = self.aggregate(Sum('amount')).get('amount__sum', 0)
        if value is None: return 0
        return value
