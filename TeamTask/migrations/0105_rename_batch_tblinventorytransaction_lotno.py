# Generated by Django 3.2.9 on 2022-01-11 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0104_auto_20220111_1256'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tblinventorytransaction',
            old_name='batch',
            new_name='lotno',
        ),
    ]
