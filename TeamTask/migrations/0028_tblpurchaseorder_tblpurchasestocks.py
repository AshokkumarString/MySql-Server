# Generated by Django 3.2.5 on 2021-11-02 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0027_auto_20211030_1023'),
    ]

    operations = [
        migrations.CreateModel(
            name='TblPurchaseorder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(blank=True, null=True)),
                ('companyid', models.CharField(blank=True, max_length=100, null=True)),
                ('total', models.CharField(blank=True, max_length=100, null=True)),
                ('supplier', models.CharField(blank=True, max_length=100, null=True)),
                ('payment', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'tbl_purchaseorder',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TblPurchasestocks',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('purchaseid', models.DateField(blank=True, null=True)),
                ('companyid', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity', models.CharField(blank=True, max_length=100, null=True)),
                ('rate', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('purchasestockid', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='purchasestock', to='TeamTask.tbltasklist')),
            ],
            options={
                'db_table': 'tbl_purchasestocks',
                'managed': True,
            },
        ),
    ]
