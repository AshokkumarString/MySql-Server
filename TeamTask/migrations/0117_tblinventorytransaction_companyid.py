# Generated by Django 3.1.1 on 2022-01-18 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0116_tblinventorytransaction_task_invoiceno'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblinventorytransaction',
            name='companyid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
