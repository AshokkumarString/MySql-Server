# Generated by Django 3.2.9 on 2022-01-07 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0096_auto_20220106_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblvouchermanagement',
            name='amount',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
