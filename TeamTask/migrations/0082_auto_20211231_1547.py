# Generated by Django 3.2.9 on 2021-12-31 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0081_tblsales_roundoff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tblvouchermanagement',
            name='purchase',
        ),
        migrations.RemoveField(
            model_name='tblvouchermanagement',
            name='salesid',
        ),
        migrations.AddField(
            model_name='tblvouchermanagement',
            name='detailsubtype',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tblvouchermanagement',
            name='detailtype',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='TblVoucherdetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('purchase', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='purchase', to='TeamTask.tblpurchaseorder')),
                ('salesid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='salesid', to='TeamTask.tblsales')),
                ('vouchermanagement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vouchermanagement', to='TeamTask.tblvouchermanagement')),
            ],
        ),
    ]