from django.shortcuts import get_object_or_404
from celery import shared_task
from django.apps import apps
from boto3 import session

from lmcservice.mailer import Mailer
from django.conf import settings

from django.templatetags.static import static
import xlsxwriter
import uuid
import os

session = session.Session()
client = session.client('s3', region_name=settings.AWS_S3_REGION,
                        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)


@shared_task
def operation(pk):
    Operation = apps.get_model("service", "operation")
    obj = get_object_or_404(Operation, id=pk)
    obj.cost = obj.total()
    obj.save()
    print(f"Cost {obj.id} updated")


@shared_task
def paid(pk):
    Operation = apps.get_model("service", "operation")
    Transaction = apps.get_model("wallet", "transaction")
    obj = get_object_or_404(Operation, id=pk)
    if obj.status != Operation.PAID and obj.payment_method != Operation.WALLET: return
    ts = Transaction.objects.filter(company=obj.company, amount__lt=0, description__endswith=f"{obj.id}")
    if ts.exists(): return
    obj, created = Transaction.objects.get_or_create(company=obj.company, amount=-1 * obj.cost,
                                                     description=f"Account debited of {obj.cost} for the payment of "
                                                                 f"ATM #{obj.id}", method=Transaction.WALLET)
    if created: print(f"Obj {obj.id} created")


@shared_task
def mailer(app, model, pk, template, subject, to):
    model = apps.get_model(app, model)
    context = model.objects \
        .values(*[field.name for field in model._meta.get_fields()]).filter(id=pk).first()
    Mailer(template, context, subject, to).send()


def worksheet_filename_path():
    if not os.path.exists(os.path.join("media/report")):
        os.mkdir(os.path.join("media/report"))
    # Create a new Excel file and add a worksheet.
    filename = "{}.xlsx".format(str(uuid.uuid4()))
    path = os.path.join("media/report", filename)
    return filename, path


@shared_task
def report(app, model, query, email):
    if app is None or model is None or query is None or email is None:
        return

    model = apps.get_model(app, model)
    print(query)
    qs = model.objects.filter(**query)

    filename, path = worksheet_filename_path()
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()

    # fields
    fields = [field for field in model._meta.get_fields() if field.name in model.list_export_fields]

    bold = workbook.add_format({'bold': True})
    for index, field in enumerate(fields):
        worksheet.write(0, index, str(field.verbose_name), bold)

    # fill data to table
    for row, obj in enumerate(qs):
        for column, field in enumerate(fields):
            worksheet.write(row + 1, column, str(getattr(obj, field.name)))
    workbook.close()
    client.upload_file(path, settings.AWS_STORAGE_BUCKET_NAME, path)
    path = static(path)

    Mailer("email/report.html", {
        "report": {"url": path}
    }, "Report", [email]).send()
