# Generated by Django 3.2.5 on 2021-11-11 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0034_tblstock_productcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbltransaction',
            name='deliverynoteid',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]