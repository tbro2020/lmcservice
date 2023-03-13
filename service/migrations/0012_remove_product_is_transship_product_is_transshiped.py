# Generated by Django 4.1.7 on 2023-03-07 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0011_remove_product_is_transshipment_product_is_transship'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_transship',
        ),
        migrations.AddField(
            model_name='product',
            name='is_transshiped',
            field=models.BooleanField(default=False, verbose_name='Is transshiped'),
        ),
    ]
