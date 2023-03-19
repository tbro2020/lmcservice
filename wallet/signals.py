from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from wallet.models import Transaction
from wallet import tasks


@receiver(post_save, sender=Transaction)
def post_save_transaction(sender, instance, created, **kwargs):
    tasks.solde.delay(instance.company_id)


@receiver(post_delete, sender=Transaction)
def post_delete_transaction(sender, instance, using,  **kwargs):
    tasks.solde.delay(instance.company_id)
