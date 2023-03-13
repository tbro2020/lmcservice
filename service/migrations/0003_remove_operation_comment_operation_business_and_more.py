# Generated by Django 4.1.7 on 2023-03-05 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_product_created_by_alter_business_is_active_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operation',
            name='comment',
        ),
        migrations.AddField(
            model_name='operation',
            name='business',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='service.business'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Created'), ('SUBMITTED', 'Submitted'), ('PRE-VALIDATE', 'Pre-Validate'), ('VALIDATE', 'Validate'), ('IN_REVIEW', 'In review'), ('COMPLETED', 'Completed')], default='CREATED', help_text='CREATED : NEW OPERATION <br/> VALIDATE: VERIFIED OPERATION REQUIRE PAYMENT <br/> IN REVIEW: NEED REVIEW OR FUTHER INFORMATION FROM CLIENT; <br/> COMPLETED: PAID OPERATION', max_length=12, verbose_name='Status'),
        ),
    ]