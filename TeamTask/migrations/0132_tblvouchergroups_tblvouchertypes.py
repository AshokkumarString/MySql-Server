# Generated by Django 3.2.9 on 2022-01-31 05:44

from django.db import migrations, models
import django.db.models.deletion
# import sqlalchemy.sql.expression


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0131_delete_tbldetailstype'),
    ]

    operations = [
        migrations.CreateModel(
            name='TblVouchergroups',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('vouchergroupname', models.CharField(blank=True, max_length=255, null=True)),
                ('isvisible', models.BooleanField(default=False)),
                ('isdeleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TblVouchertypes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('vouchertypename', models.CharField(blank=True, max_length=255, null=True)),
                ('vouchertypereferencename', models.CharField(blank=True, max_length=255, null=True)),
                ('vouchertypegroup', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vouchertypegroup', to='TeamTask.tblvouchergroups')),
            ],
        ),
    ]