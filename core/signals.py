from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from core.models import *

from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings


@receiver(post_save, sender=User)
def user(sender, instance, created, **kwargs):
    if not created: return
    form = PasswordResetForm({"email": instance.email})
    if form.is_valid():
        form.save(domain_override=settings.HOSTNAME)
