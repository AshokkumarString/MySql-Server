# Generated by Django 3.2.9 on 2021-12-16 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0068_tblexpenses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblexpenses',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
