# Generated by Django 3.2.5 on 2022-01-04 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0090_tblsalestransaction_usedqty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblpurchaseorder',
            name='advancepaid',
            field=models.CharField(blank=True, default=0, max_length=100),
        ),
        migrations.AlterField(
            model_name='tblsales',
            name='advancereceived',
            field=models.CharField(blank=True, default=0, max_length=100),
        ),
    ]
