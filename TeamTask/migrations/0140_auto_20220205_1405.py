# Generated by Django 3.2.9 on 2022-02-05 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0139_merge_20220205_1405'),
    ]

    operations = [

        migrations.AlterField(
            model_name='tblpurchasestocks',
            name='received',
            field=models.CharField(blank=True, default=0,
                                   max_length=100, null=True),
        ),
    ]
