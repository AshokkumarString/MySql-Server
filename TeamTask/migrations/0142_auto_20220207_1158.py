# Generated by Django 3.2.9 on 2022-02-07 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0141_merge_0140_auto_20220205_1305_0140_auto_20220205_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblquotationrequest',
            name='salesorderid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tblquotationrequest',
            name='users',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
