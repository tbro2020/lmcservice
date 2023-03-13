# Generated by Django 4.1.7 on 2023-03-05 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_delete_operationmanifest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operation',
            name='arrival',
        ),
        migrations.RemoveField(
            model_name='operation',
            name='departure',
        ),
        migrations.RemoveField(
            model_name='operation',
            name='penality',
        ),
        migrations.RemoveField(
            model_name='operation',
            name='ship_name',
        ),
        migrations.RemoveField(
            model_name='operation',
            name='shipowner',
        ),
        migrations.RemoveField(
            model_name='operation',
            name='trip_nber',
        ),
        migrations.AlterField(
            model_name='operation',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Created'), ('SUBMITTED', 'Submitted'), ('PRE-VALIDATE', 'Pre-Validate'), ('VALIDATE', 'Validate'), ('IN_REVIEW', 'In review'), ('COMPLETED', 'Completed')], default='CREATED', max_length=12, verbose_name='Status'),
        ),
    ]