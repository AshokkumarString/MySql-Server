# Generated by Django 3.2.9 on 2021-12-07 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0049_auto_20211207_1144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tblstock',
            old_name='cgstpercentange',
            new_name='cgstpercentage',
        ),
    ]