# Generated by Django 3.2.5 on 2022-01-22 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0118_auto_20220119_1503'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TblTransactTable',
        ),
        migrations.AddField(
            model_name='tblclient',
            name='gstnumber',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tblclient',
            name='pannumber',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
