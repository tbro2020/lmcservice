from django.db.models.signals import pre_save, post_save
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver

from service.models import *
from service import task


@receiver(pre_save, sender=Product)
def pre_product(sender, instance, raw, using, update_fields, **kwargs):
    total = instance.product_type.fees * instance.quantity
    if instance.penalty > 0:
        total = total + (total * (instance.penalty / 100))
    instance.total = total


@receiver(post_save, sender=Product)
def post_product(sender, instance, created, **kwargs):
    task.operation.delay(instance.operation_id)


@receiver(post_save, sender=Company)
def post_company(sender, instance, created, **kwargs):
    model = instance._meta
    if created:
        task.mailer.delay(model.app_label, model.model_name, instance.id,
                          "email/company/welcome.html", _("Thank you for your registration"),
                          instance.email)
        return

    qs = User.objects.filter(company=instance)
    if qs.exists():
        qs.update(is_active=instance.is_active)
        return
    if not instance.is_active: return
    User.objects.create_user(instance.email, company=instance, is_active=True)
