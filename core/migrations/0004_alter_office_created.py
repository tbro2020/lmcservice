# Generated by Django 4.1.7 on 2023-03-26 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='office',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Créé'),
        ),
    ]
