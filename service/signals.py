from django.db.models.signals import pre_save, post_save
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver

from django.contrib.auth.models import Group, Permission

from service.models import *
from service import tasks

from datetime import date


@receiver(pre_save, sender=Product)
def pre_product(sender, instance, raw, using, update_fields, **kwargs):
    total = instance.product_type.fees * instance.quantity
    total = total + (total * (instance.penalty / 100))
    instance.total = total


@receiver(post_save, sender=Product)
def post_product(sender, instance, created, **kwargs):
    tasks.operation.delay(instance.operation_id)


@receiver(post_save, sender=Company)
def post_company(sender, instance, created, **kwargs):
    model = instance._meta
    if created:
        tasks.mailer.delay(model.app_label, model.model_name, instance.id,
                          "email/company/welcome.html", _("Thank you for your registration"),
                          instance.email)
        return

    qs = User.objects.filter(company=instance)
    if qs.exists():
        qs.update(is_active=instance.is_active)
        return
    if not instance.is_active: return
    user = User.objects.create_user(instance.email, password=f"Default@LMC-{date.today().year}",
                                    company=instance, is_active=True)
    group, created = Group.objects.get_or_create(name="Forwarder")
    if created:
        permissions = Permission.objects.filter(codename__in=["add_user", "view_user", "change_user", "delete_user",
                                                              "add_operation", "view_operation", "change_operation",
                                                              "delete_operation"])
        group.permissions.add(*list(permissions))
    user.groups.add(group)
