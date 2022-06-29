# Generated by Django 3.2.9 on 2022-02-01 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0136_tblcompany_isgst'),
    ]

    operations = [
        migrations.CreateModel(
            name='TblLedgergroups',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ledgergroupname', models.CharField(
                    blank=True, max_length=255, null=True)),
                ('isvisible', models.BooleanField(default=False)),
                ('isdeleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'tbl_ledgergroup',
                'managed': (True,),
            },
        ),
        migrations.CreateModel(
            name='TblLedgertypes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ledgertypename', models.CharField(
                    blank=True, max_length=255, null=True)),
                ('isvisible', models.BooleanField(default=False)),
                ('ledgertypegroup', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                 related_name='ledgertypegroup', to='TeamTask.tblledgergroups')),
            ],
            options={
                'db_table': 'tbl_ledgertype',
                'managed': (True,),
            },
        ),
        migrations.DeleteModel(
            name='TblVouchergroups',
        ),
        migrations.DeleteModel(
            name='TblVouchertypes',
        ),
    ]
