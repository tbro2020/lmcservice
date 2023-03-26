# Generated by Django 4.1.7 on 2023-03-26 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_historicaluser_historicalunit_historicalproducttype_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalbordercrossing',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalnotification',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalnotification',
            name='user',
        ),
        migrations.RemoveField(
            model_name='historicaloffice',
            name='billing_info',
        ),
        migrations.RemoveField(
            model_name='historicaloffice',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalport',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalproducttype',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalproducttype',
            name='unit',
        ),
        migrations.RemoveField(
            model_name='historicalunit',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaluser',
            name='company',
        ),
        migrations.RemoveField(
            model_name='historicaluser',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaluser',
            name='office',
        ),
        migrations.AlterField(
            model_name='office',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Création'),
        ),
        migrations.DeleteModel(
            name='HistoricalBillingInfo',
        ),
        migrations.DeleteModel(
            name='HistoricalBorderCrossing',
        ),
        migrations.DeleteModel(
            name='HistoricalNotification',
        ),
        migrations.DeleteModel(
            name='HistoricalOffice',
        ),
        migrations.DeleteModel(
            name='HistoricalPort',
        ),
        migrations.DeleteModel(
            name='HistoricalProductType',
        ),
        migrations.DeleteModel(
            name='HistoricalUnit',
        ),
        migrations.DeleteModel(
            name='HistoricalUser',
        ),
    ]
