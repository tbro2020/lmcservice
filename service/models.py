from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField

from core.models import *
from django_countries.fields import CountryField

from django.db.models import Sum


def upload_directory_file(instance, filename):
    return '{0}/{1}/{2}'.format(instance._meta.app_label, instance._meta.model_name, filename)


class Company(models.Model):
    name = models.CharField(_("Company name"), max_length=50)
    # business_type = models.ForeignKey(BusinessType, on_delete=models.CASCADE)

    email = models.EmailField(_('Email address'), unique=True)
    phone_number = PhoneNumberField(help_text=_("+243XXXXXXXXX"))

    address = models.TextField(_("Address"))
    city = models.CharField(_("City"), max_length=50)
    country = CountryField(verbose_name=_("Country"))
    postal_code = models.CharField(_("Postal Code"), max_length=50)

    # users = models.ManyToManyField(User, blank=True)
    is_active = models.BooleanField(_("Activate"), help_text=_("By activating/desactivating all account linked will "
                                                               "impacted"), default=False)
    term_condition = models.BooleanField(_(" I read & accept the terms & conditions"),
                                         help_text=_("Aware of term and condition"), default=True)

    balance = MoneyField(verbose_name=_("Solde"), max_digits=14, decimal_places=2, default_currency='USD', default=0.0)

    updated = models.DateTimeField(_("Updated"), auto_now=True)
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    form_fields = ("name", "email", "phone_number", "address",
                   "city", "country", "postal_code", "country",
                   "term_condition")

    list_display_fields = ("id", "name", "country", "balance", "is_active")

    change_actions = ({
                          "verbose_name": "Activate",
                          "method": "POST",
                          "url": reverse("core:action", kwargs={"app": "service", "model": "company", "verbose": "Activate"}),
                          "permission": "service.change_company",
                          "limitation": {"is_active": False},
                          "values": {"is_active": True},
                          "condition": "request.user.is_staff"
                      }, {
                          "verbose_name": "Dis-activate",
                          "method": "POST",
                          "url": reverse("core:action", kwargs={"app": "service", "model": "company", "verbose": "Dis-activate"}),
                          "permission": "service.change_company",
                          "limitation": {"is_active": True},
                          "values": {"is_active": False},
                          "condition": "request.user.is_staff"
                      })

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        unique_together = ("name", "email", "phone_number")


class Operation(models.Model):
    IMPORTATION = "Importation"
    EXPORTATION = "Exportation"

    TYPE_OPERATIONS = (
        (IMPORTATION, _('Importation')),
        (EXPORTATION, _('Exportation')),
    )

    CREATED = "CREATED"
    SUBMITTED = "SUBMITTED"
    PREVALIDATE = "PRE-VALIDATE"
    VALIDATE = "VALIDATE"
    IN_REVIEW = "IN_REVIEW"
    PAID = "PAID"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"

    STATUS = (
        (CREATED, _('Created')),
        (SUBMITTED, _('Submitted')),
        (PREVALIDATE, _('Pre-Validate')),
        (VALIDATE, _('Validate')),
        (IN_REVIEW, _('In review')),
        (COMPLETED, _('Completed')),  # only been activated by the dept. financial user
        (PAID, _("Paid")),
        (REJECTED, _('Rejected'))
    )

    WALLET = "WALLET"
    PROOF = "PROOF OF PAYMENT"

    PAYMENT_METHOD = (
        (WALLET, _('Provision')),
        (PROOF, _('Proof of Payment')),
    )

    BOAT = "VESSEL"
    TRUCK = "TRUCK"
    TRAIN = "TRAIN"

    TRANSPORT_TYPE = (
        (BOAT, _('Vessel')),
        (TRUCK, _('Truck')),
        (TRAIN, _('Train'))
    )

    transport = models.CharField(_("Transport"), max_length=50, choices=TRANSPORT_TYPE, default=BOAT)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=None, null=True, blank=True)
    operation_type = models.CharField(_("Operation Type"), max_length=12, choices=TYPE_OPERATIONS)

    importer_expoter = models.CharField(_("Importator/Exportator"), max_length=100, blank=True, null=True, default=None)
    forwarder = models.CharField(_("Forwarder/Shipping Agent"), max_length=99, blank=True, null=True, default=None)

    entry_point = models.ForeignKey(Port, verbose_name=_("Origin point"), on_delete=models.CASCADE,
                                    related_name="entry_point", null=True, default=None)
    load_point = models.ForeignKey(Port, verbose_name=_("Load port"), on_delete=models.CASCADE,
                                   related_name="load_point", null=True, default=None)
    unload_point = models.ForeignKey(Port, verbose_name=_("Discharge port"), on_delete=models.CASCADE,
                                     related_name="unload_point", null=True, default=None)
    exit_point = models.ForeignKey(BorderCrossing, verbose_name=_("Border crossing"), on_delete=models.CASCADE,
                                   related_name="unload_point", null=True, default=None)
    end_point = models.CharField(max_length=100, null=True, default=None)

    export_permit = models.FileField(_("Export Permit"), upload_to=upload_directory_file,
                                     help_text=_("Format supported : pdf"),
                                     validators=[FileExtensionValidator(['pdf'])], blank=True, null=True, default=None)

    cost = MoneyField(verbose_name=_("Cost($)"), max_digits=14, decimal_places=2, default_currency='USD',
                      null=True, blank=True, default=None)

    status = models.CharField(_("Status"), max_length=12, choices=STATUS, default=CREATED)

    manifest_bp_no = models.CharField(_("Manifest/BP n°"), max_length=50, null=True, default=None)
    bp_file = models.FileField(_("BP/Manifest Document"), upload_to=upload_directory_file,
                               help_text=_("Format supported : pdf, jpg, jpeg, png"),
                               validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'pdf', 'xls'])], blank=True,
                               null=True, default=None)

    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD, blank=True, null=True, default=None)
    proof_of_payment = models.FileField(_("Proof of payment"), upload_to=upload_directory_file,
                                        help_text=_("Format supported : pdf,jpg,jpeg,png"),
                                        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])], blank=True,
                                        null=True, default=None)

    updated_by = models.ForeignKey(User, related_name="updated_by", null=True, blank=True, default=None,
                                   on_delete=models.SET_NULL)
    updated = models.DateTimeField(_("Updated"), auto_now=True)

    created_by = models.ForeignKey(User, related_name="created_by", null=True, blank=True, default=None,
                                   on_delete=models.SET_NULL)
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        unique_together = ('ship_name', 'trip_nber')

    def __str__(self):
        return f"OP_{self.transport}_{self.id}"

    """
    def clean(self):
        if self.status not in [Operation.VALIDATE, Operation.COMPLETED]: return
        # if not self.has_final_manifest(): raise ValidationError("Please make sure the latest manifest is provided")
        if not bool(self.manifest_bp_no): raise ValidationError("Please make sure you fill the Manifest BP N.")
        # if self.product_count() == 0: raise ValidationError("The system could not validate an operation with no products")

        if self.status == Operation.COMPLETED:
            if self.payment_method == Operation.PROOF and not bool(self.proof_of_payment):
                raise ValidationError("Please provide a valid proof of payment")
    """

    form_fields = ("transport", "operation_type", "forwarder", "bp_file",
                   "importer_expoter", "load_point", "entry_point", "exit_point")

    filter_fields = ("transport", "status", "load_point", "entry_point", "exit_point", "updated", "created")

    editable_if = "(not request.user.is_staff and obj.status == 'CREATED') or (request.user.is_staff) or (" \
                  "request.user.is_superuser)"

    extra = {
        "fields": ({
           "condition": "request.user.is_staff",
           "name": "status"
        }, {
            "condition": "request.user.is_staff",
            "name": "proof_of_payment"
        })
    }

    list_export_fields = ("id", "company", "status", "cost", "payment_method", "created")
    list_display_fields = ("id", "company", "status", "cost", "payment_method")
    inline_model_form = {"app_label": "service", "model_name": "Product"}

    change_actions = ({
          "verbose_name": "Debit Note",
          "method": "GET",
          "url": reverse("core:document",
                         kwargs={"app": "service", "model": "operation", "template": "invoice"}),
          "permission": "service.view_operation",
          "limitation": {"status": VALIDATE},
          "condition": "1"
      }, {
          "verbose_name": "ATM",
          "method": "GET",
          "url": reverse("core:document",
                         kwargs={"app": "service", "model": "operation", "template": "atm"}),
          "permission": "service.view_operation",
          "limitation": {"status": COMPLETED},
          "condition": "1"
      }, {
          "verbose_name": "Checkpoint",
          "method": "GET",
          "url": reverse("core:list", kwargs={"app": "service", "model": "checkpoint"}),
          "permission": "service.view_checkpoint",
          "limitation": {"status": COMPLETED},
          "condition": "1"
      }, {
        "verbose_name": "Pay",
        "method": "POST",
        "url": reverse("core:action", kwargs={"app": "service", "model": "operation", "verbose": "Pay"}),
        "permission": "service.change_operation",
        "limitation": {"status": VALIDATE},
        "condition": "not request.user.is_staff",
        "values": {"status": PAID, "payment_method": WALLET},
        "prerequisite": {
            "condition": "apps.get_model('wallet', 'transaction').objects.filter(company=qs.last().company, "
                         "status='PAID').balance() > qs.last().cost.amount",
            "action": "apps.get_model('wallet', 'transaction').debit(qs.last())",
            "message": {
                "error": "We fail to debit your account",
                "success": "Your account has been debited with success"
            }
        }
      }, {
          "verbose_name": "Submit",
          "method": "POST",
          "url": reverse("core:action", kwargs={"app": "service", "model": "operation", "verbose": "Submit"}),
          "permission": "service.change_operation",
          "limitation": {"status": CREATED},
          "values": {"status": SUBMITTED},
          "condition": "not request.user.is_staff"
    })

    list_actions = ({
        "verbose_name": "Export",
        "permission": "service.view_operation",
        "url": reverse("core:export", kwargs={"app": "service", "model": "operation"})
    },)

    def total(self):
        qs = Product.objects.values('total').filter(operation=self)
        _total = qs.aggregate(Sum('total')).get('total__sum', 0)
        if _total is None: return 0
        return _total

    class Meta:
        verbose_name = _("Operation")
        verbose_name_plural = _("Operations")


# -----------------------------------------------------------

class Product(models.Model):
    name = models.CharField(_("Product's nature"), max_length=50)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)

    product_type = models.ForeignKey(ProductType, verbose_name=_("Product type"), on_delete=models.CASCADE)
    quantity = models.FloatField(_("Quantity/Weight"))

    description = models.TextField(_("Description"), default="-")
    attach = models.FileField(_("Attach"), upload_to=upload_directory_file, blank=True, null=True, default=None,
                              max_length=100)

    ref = models.CharField(_("Ref. Lot"), max_length=50, null=True, default=None)
    truck = models.CharField(_("Truck"), max_length=50, null=True, default=None)
    destination = models.CharField(_("Destination"), max_length=50, null=True, default=None)

    # Extra field of control
    penalty = models.IntegerField(_("Penalty applied"), help_text=_("The penalty is applied in %"), null=True, default=0)
    total = MoneyField(verbose_name=_("Total($)"), max_digits=14, decimal_places=2, null=True, default=None,
                       default_currency='USD')

    is_transshipped = models.BooleanField(_("Is transshipped"), null=True, default=False)

    is_activated = models.BooleanField(_("Is activated"), null=True, help_text=_("This ATM is active"), default=True)

    updated_by = models.ForeignKey(User, related_name="product_updated_by", null=True, blank=True, default=None,
                                   on_delete=models.SET_NULL)

    updated = models.DateTimeField(_("Updated"), auto_now=True)

    created_by = models.ForeignKey(User, related_name="product_created_by", null=True, blank=True, default=None,
                                   on_delete=models.SET_NULL)
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    form_fields = ("operation", "product_type", "quantity",
                   "name", "destination", "ref", "truck")

    extra = {
        "fields": ({
                       "condition": "request.user.is_superuser",
                       "name": "penalty"
                   }, {
                       "condition": "request.user.is_superuser",
                       "name": "is_activated"
                   })
    }

    list_display_fields = ("id", "operation", "product_type", "quantity", "destination", "is_activated")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Product/Cargo")
        verbose_name_plural = _("Product/Cargos")


class CheckPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, null=True, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, default=None)

    location = models.JSONField(null=True, default=None)
    device_info = models.JSONField(null=True, default=None)

    created = models.DateTimeField(_("Created"), auto_now_add=True)

    def url(self, request):
        return "https://{host}{path}".format(host=request.get_host(), path=reverse("service:check-point-operation",
                                                                                   kwargs={"checkpoint": self.id}))

    class Meta:
        verbose_name = _("Check point")
        verbose_name_plural = _("Check points")

    list_display_fields = ("id", "operation", "product", "created")
