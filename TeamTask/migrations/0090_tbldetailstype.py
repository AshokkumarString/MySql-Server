# Generated by Django 3.2.9 on 2022-01-04 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0089_remove_tblsalesdispatch_salesinvoiceno'),
    ]

    operations = [
        migrations.CreateModel(
            name='TblDetailstype',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('vouchertype', models.CharField(blank=True, max_length=255, null=True)),
                ('detailtype', models.CharField(blank=True, max_length=255, null=True)),
                ('detailsubtype', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'tbl_detailstype',
                'managed': (True,),
            },
        ),
    ]
