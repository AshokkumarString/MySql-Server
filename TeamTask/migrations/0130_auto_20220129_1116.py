# Generated by Django 3.2.5 on 2022-01-29 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0129_auto_20220128_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblinventorytransaction',
            name='hsncode',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='tblsalestransaction',
            name='hsncode',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
