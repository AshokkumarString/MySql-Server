# Generated by Django 3.1.1 on 2022-01-12 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0111_remove_tblinventorytransaction_lotno'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TblTransactionOverview',
        ),
    ]