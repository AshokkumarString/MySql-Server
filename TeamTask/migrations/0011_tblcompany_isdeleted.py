# Generated by Django 3.2.5 on 2021-09-29 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0010_auto_20210924_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblcompany',
            name='isdeleted',
            field=models.BooleanField(default=True),
        ),
    ]