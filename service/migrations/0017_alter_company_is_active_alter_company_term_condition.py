# Generated by Django 4.1.7 on 2023-03-08 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0016_remove_company_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='is_active',
            field=models.BooleanField(default=False, help_text='By activating/desactivating all account linked will impacted', verbose_name='Activate'),
        ),
        migrations.AlterField(
            model_name='company',
            name='term_condition',
            field=models.BooleanField(default=True, help_text='Aware of term and condition', verbose_name=' I read & accept the terms & conditions'),
        ),
    ]