# Generated by Django 4.1.7 on 2023-03-07 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_office_access_alter_office_limitation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='office',
            name='access',
        ),
    ]
