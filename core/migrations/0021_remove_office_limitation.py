# Generated by Django 4.1.7 on 2023-03-07 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_office_limitation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='office',
            name='limitation',
        ),
    ]
