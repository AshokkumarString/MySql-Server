# Generated by Django 3.2.5 on 2022-06-14 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0162_auto_20220611_1737'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tbltransaction',
            old_name='companyid',
            new_name='companyidnum',
        ),
    ]