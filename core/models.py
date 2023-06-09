from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.db import models

from djmoney.models.fields import MoneyField
from core.utils import default_limitation
from core.manager import UserManager


class User(AbstractUser):
    username = None
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    company = models.ForeignKey('service.Company', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    office = models.ForeignKey('Office', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    email = models.EmailField(unique=True)

    objects = UserManager()

    list_display_fields = ("id", "first_name", "last_name", "email", "company__name", "office__name", "is_active")
    form_fields = ("last_name", "first_name", "email", "is_active")
    # filter_fields = ("company", "office")

    extra = {
        "fields": ({
                       "condition": "request.user.is_staff",
                       "name": "office"
                   }, {
                       "condition": "request.user.is_staff",
                       "name": "company"
                   }, {
                       "condition": "request.user.is_staff",
                       "name": "is_staff"
                   }, {
                       "condition": "request.user.is_staff",
                       "name": "is_superuser"
                   }, {
                       "condition": "request.user.is_staff",
                       "name": "groups"
                   })
    }

    def __str__(self):
        return self.email


class Port(models.Model):
    name = models.CharField(_("name"), max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Port")
        verbose_name_plural = _("Ports")


class BillingInfo(models.Model):
    name = models.CharField(_("Name"), max_length=50)

    address = models.TextField(_("Address"))
    city = models.CharField(_("City"), max_length=50)
    country = models.CharField(_("Country"), max_length=50)
    postal_code = models.CharField(_("Postal Code"), max_length=50)

    account_no = models.CharField(_("Account no"), max_length=50)
    bank_name = models.CharField(_("Bank name"), max_length=50)
    branch_name = models.CharField(_("Branch name"), max_length=50)
    branch_no = models.CharField(_("Branch no"), max_length=50)
    swift_code = models.CharField(_("Swift code"), max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Billing Information")
        verbose_name_plural = _("Billing Informations")

    list_display_fields = ("id", "name", "city", "country")


class Office(models.Model):
    IMPORTATION = "Importation"
    EXPORTATION = "Exportation"
    TYPE_OPERATIONS = ((IMPORTATION, _('Importation')), (EXPORTATION, _('Exportation')),)

    name = models.CharField(max_length=100)
    supervisor = models.CharField(_("Supervisor Full Name"), max_length=100)
    billing_info = models.ForeignKey(BillingInfo, on_delete=models.CASCADE, null=True, default=None)

    limitation = models.JSONField(default=default_limitation)

    updated = models.DateTimeField(_("Updated"), auto_now=True)
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    form_fields = ("name", "billing_info", "supervisor", "limitation")
    list_display_fields = ("id", "name", "supervisor", "billing_info__name")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Office")
        verbose_name_plural = _("Offices")


class BorderCrossing(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    list_display_fields = ("id", "name")

    class Meta:
        verbose_name = _("Border Crossing")
        verbose_name_plural = _("Border(s) Crossing")


class Unit(models.Model):
    name = models.CharField(_("name"), max_length=50)
    abbreviation = models.CharField(_("Abbreviation"), max_length=50)

    def __str__(self):
        return self.name

    list_display_fields = ("id", "name", "abbreviation")

    class Meta:
        verbose_name = _("Product Unit")
        verbose_name_plural = _("Product Unit(s)")


# -----------------------------------------------------------
class ProductType(models.Model):
    name = models.CharField(_("name"), max_length=150)

    fees = MoneyField(verbose_name=_("Fees($)"), max_digits=14, decimal_places=2, default_currency='USD')
    fees_admin = MoneyField(verbose_name=_("Admin Fees($)"), max_digits=14, decimal_places=2, default_currency='USD')

    unit = models.ForeignKey(Unit, verbose_name=_("Unit"), on_delete=models.CASCADE)

    def __str__(self):
        return "({unit}) {name}".format(unit=self.unit.name, name=self.name)

    list_display_fields = ("id", "fees", "unit")

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Type(s)")


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    created = models.DateTimeField(auto_created=True)
