# Generated by Django 3.2.5 on 2022-02-04 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0136_tblcompany_isgst'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblsalesrequest',
            name='clientid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tblsalesrequest',
            name='companyid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
