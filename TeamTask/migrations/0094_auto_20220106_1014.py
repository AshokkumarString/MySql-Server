# Generated by Django 3.2.9 on 2022-01-06 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0093_auto_20220105_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblpurchasebillinvoice',
            name='amountreceived',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tblsalesdispatch',
            name='receivedamount',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
