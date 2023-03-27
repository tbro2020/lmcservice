from django.db import models
from djmoney.models.fields import MoneyField
from django.utils.translation import gettext_lazy as _

from service.models import Company
from wallet.manager import TransactionQuerySet
from django.core.validators import FileExtensionValidator


def upload_directory_file(instance, filename):
    return '{0}/{1}/{2}'.format(instance._meta.app_label, instance._meta.model_name, filename)


class Transaction(models.Model):
    PAID = "PAID"
    UNPAID = "UNPAID"
    IN_REVIEW = "IN_REVIEW"

    STATUS = (
        (PAID, _('Paid')),
        (UNPAID, _('Unpaid')),
        (IN_REVIEW, _('In review')),
    )

    CASH = "CASH"
    WALLET = "WALLET"
    DEPOSIT = "DEPOSIT"

    METHOD = (
        (CASH, _('CASH')),
        (DEPOSIT, _('DEPOSIT')),
        (WALLET, _('WALLET')),
    )

    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)
    amount = MoneyField(verbose_name=_("Amount"), max_digits=14, decimal_places=2, default_currency='USD')

    method = models.CharField(max_length=30, choices=METHOD)
    description = models.TextField(_("description"), default="-")
    status = models.CharField(_("Status"), max_length=12, choices=STATUS, default=UNPAID)
    proof_of_payment = models.FileField(_("Proof of payment"), upload_to=upload_directory_file,
                                        help_text=_("Format supported : pdf,jpg,jpeg,png"),
                                        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])], blank=True,
                                        null=True, default=None)

    created = models.DateTimeField(_("Created"), auto_now_add=True)

    objects = TransactionQuerySet.as_manager()

    @staticmethod
    def debit(obj):
        obj, created = Transaction.objects \
            .get_or_create(company=obj.company, amount=-1 * obj.cost,
                           status=Transaction.PAID, method=Transaction.WALLET,
                           description=f"Account debited of {obj.cost} for the payment of ATM #{obj.id}")
        return obj

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")

    form_fields = ("company", "amount", "method", "proof_of_payment", "description", "status")
    list_display_fields = ("id", "company__name", "amount", "method", "status", "created")
    filter_fields = ("status", "created")
