# Generated by Django 3.2.5 on 2022-06-18 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0163_rename_companyid_tbltransaction_companyidnum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tblinvoicesummary',
            name='client',
        ),
        migrations.RemoveField(
            model_name='tblinvoicesummary',
            name='companyid',
        ),
        migrations.RemoveField(
            model_name='tbltransaction',
            name='clientid',
        ),
        migrations.RemoveField(
            model_name='tbltransaction',
            name='companyidnum',
        ),
        migrations.RemoveField(
            model_name='tbltransaction',
            name='taskid',
        ),
    ]
