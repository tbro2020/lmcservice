from django_json_widget.widgets import JSONEditorWidget
from djmoney.models import fields
from django.db import models


def modelform_factory_data(model):
    return {"fields": list(
        getattr(model, "form_fields", [field.name for field in model._meta.get_fields() if type(field) in [
            models.CharField, models.IntegerField, models.FloatField, models.BooleanField,
            models.JSONField, models.ForeignKey, models.ManyToManyField, fields.MoneyField
        ]])),
        "exclude": ['created'],
        "widgets": {field.name: JSONEditorWidget for field in model._meta.fields if
                    field.get_internal_type() == 'JSONField'}
    }


def default_limitation():
    return {
        "field": {
            "company": {
                "city": None,
                "country": None
            },
            "operation": {field: None for field in ["transport", "company", "operation_type",
                                                    "entry_point", "load_point", "unload_point",
                                                    "exit_point", "end_point", "status", "payment_method",
                                                    "updated_by", "updated", "created_by", "created"]}
        },
        "value": {
            "operation": {
                "status": None
            }
        }
    }
