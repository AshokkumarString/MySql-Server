# Generated by Django 3.2.5 on 2022-01-04 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0089_remove_tblsalesdispatch_salesinvoiceno'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblsalestransaction',
            name='usedqty',
            field=models.CharField(blank=True, default=0, max_length=255),
        ),
    ]