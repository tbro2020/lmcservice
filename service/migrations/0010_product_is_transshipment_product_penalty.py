# Generated by Django 4.1.7 on 2023-03-07 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0009_alter_operation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_transshipment',
            field=models.BooleanField(default=False, verbose_name='Is transshipment'),
        ),
        migrations.AddField(
            model_name='product',
            name='penalty',
            field=models.IntegerField(default=0, verbose_name='Penality applied'),
        ),
    ]