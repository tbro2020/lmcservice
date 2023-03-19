from django.db.models.signals import post_save
from django.dispatch import receiver

from wallet.models import Transaction
from wallet import tasks


@receiver(post_save, sender=Transaction)
def post_product(sender, instance, created, **kwargs):
    tasks.solde.delay(instance.company_id)
