# Generated by Django 3.2.5 on 2022-01-01 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0084_auto_20211231_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblpurchasebillinvoice',
            name='roundoff',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
