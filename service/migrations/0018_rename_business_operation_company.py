# Generated by Django 4.1.7 on 2023-03-08 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0017_alter_company_is_active_alter_company_term_condition'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operation',
            old_name='business',
            new_name='company',
        ),
    ]