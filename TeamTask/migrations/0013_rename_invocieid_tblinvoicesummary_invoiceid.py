# Generated by Django 3.2.5 on 2021-09-29 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0012_auto_20210929_1423'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tblinvoicesummary',
            old_name='invocieid',
            new_name='invoiceid',
        ),
    ]
