# Generated by Django 3.2.5 on 2021-11-11 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0033_tblinvoicesummary_deliverynoteid'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblstock',
            name='productcode',
            field=models.CharField(blank=True, db_column='ProductCode', max_length=100, null=True),
        ),
    ]
