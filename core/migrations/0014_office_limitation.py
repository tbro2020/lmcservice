# Generated by Django 4.1.7 on 2023-03-07 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_remove_office_limitation'),
    ]

    operations = [
        migrations.AddField(
            model_name='office',
            name='limitation',
            field=models.BooleanField(default=False),
        ),
    ]
