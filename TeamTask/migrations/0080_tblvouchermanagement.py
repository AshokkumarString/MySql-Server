# Generated by Django 3.2.9 on 2021-12-27 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0079_alter_tblinventorytransaction_batch'),
    ]

    operations = [
        migrations.CreateModel(
            name='TblVouchermanagement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('username', models.CharField(blank=True, max_length=250, null=True)),
                ('clientname', models.CharField(blank=True, max_length=250, null=True)),
                ('vouchertype', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('cashmode', models.CharField(blank=True, max_length=250, null=True)),
                ('companyname', models.CharField(blank=True, max_length=250, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='client', to='TeamTask.tblclient')),
                ('purchase', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='purchase', to='TeamTask.tblpurchaseorder')),
                ('salesid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='salesid', to='TeamTask.tblsales')),
            ],
            options={
                'db_table': 'tbl_vouchermanagement',
                'managed': (True,),
            },
        ),
    ]
