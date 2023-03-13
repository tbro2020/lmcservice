# Generated by Django 4.1.7 on 2023-03-08 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0017_alter_company_is_active_alter_company_term_condition'),
        ('core', '0024_user_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.company'),
        ),
        migrations.AlterField(
            model_name='user',
            name='office',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.office'),
        ),
    ]
