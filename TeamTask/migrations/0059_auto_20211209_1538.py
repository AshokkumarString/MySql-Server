# Generated by Django 3.2.5 on 2021-12-09 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0058_auto_20211209_1310'),
    ]

    operations = [
        migrations.CreateModel(
            name='TblPurchasebillinvoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(blank=True, null=True)),
                ('purchaseinvoiceno', models.CharField(blank=True, max_length=255, null=True)),
                ('supplier', models.CharField(blank=True, max_length=255, null=True)),
                ('company', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.CharField(blank=True, max_length=255, null=True)),
                ('reference', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'tbl_purchasebillinvoice',
                'managed': (True,),
            },
        ),
        migrations.DeleteModel(
            name='TblPurchaseinvoice',
        ),
        migrations.RemoveField(
            model_name='tblinventorytransaction',
            name='convertionstockname',
        ),
        migrations.RemoveField(
            model_name='tblinventorytransaction',
            name='receivedquantity',
        ),
        migrations.AddField(
            model_name='tblinventorytransaction',
            name='batch',
            field=models.CharField(blank=True, default=0, max_length=255, null=True),
        ),
    ]