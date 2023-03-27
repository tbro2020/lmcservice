from django.apps import apps
from django import template

from service.models import Operation
from datetime import timedelta

import qrcode
import base64
import qrcode.image.svg
from io import BytesIO

register = template.Library()


@register.filter(name='models')
def models(user):
    app = dict()
    for model in apps.get_models():
        if model._meta.model_name in ["session", "product"]: continue
        if model._meta.app_label not in app: app[model._meta.app_label] = []
        if user.has_perm(f"{model._meta.app_label}.view_{model._meta.model_name}"):
            app[model._meta.app_label].append({"name": model._meta.model_name, "verbose": model._meta.verbose_name})
    return {k: v for k, v in app.items() if v}


@register.filter(name='getattr')
def get_attribute(obj, attr):
    data = getattr(obj, attr, None)
    return data


@register.filter(name="getdict")
def get_dictionary(obj, key):
    return obj.get(key, None)


@register.filter(name="displaystatus")
def display_status(status):
    return {
        Operation.CREATED: "secondary",
        Operation.SUBMITTED: "dark",
        Operation.PREVALIDATE: "info",
        Operation.IN_REVIEW: "warning",
        Operation.VALIDATE: "primary",
        Operation.COMPLETED: "success",
        Operation.PAID: "success",
        Operation.REJECTED: 'danger'
    }.get(status)


@register.filter(name="attrmatch")
def attr_match(obj, limit):
    for key, value in limit.items():
        if getattr(obj, key, False) != value:
            return False
    return True


@register.filter(name="multiply")
def multiply(left, right):
    return float(left) * float(right)


@register.filter(name="divide")
def divide(left, right):
    return float(left) / float(right)


@register.filter(name="eval")
def evaluation(expression, request):
    return eval(expression)


@register.filter(name="stringbuilder")
def stringbuilder(a, b):
    return f"{str(a)}{str(b)}"


@register.filter(name="addDays")
def addDays(date, days):
    return date + timedelta(days=days)


@register.filter(name="atmQrcode")
def atmQrcode(operation, product):
    factory = qrcode.image.svg.SvgImage
    content = "{'next':'atm', 'operation': %d, 'product': %d}" % (operation, product)
    img = qrcode.make(content, image_factory=factory, box_size=20)
    stream = BytesIO()
    img.save(stream)
    base64_image = base64.b64encode(stream.getvalue()).decode()
    return 'data:image/svg+xml;utf8;base64,' + base64_image
