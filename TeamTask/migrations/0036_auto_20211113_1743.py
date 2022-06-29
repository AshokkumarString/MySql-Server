# Generated by Django 3.2.5 on 2021-11-13 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0035_tbltransaction_deliverynoteid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tblinvoicesummary',
            name='deliverynoteid',
        ),
        migrations.RemoveField(
            model_name='tbltransaction',
            name='deliverynoteid',
        ),
        migrations.AddField(
            model_name='tblinvoicesummary',
            name='quotationid',
            field=models.IntegerField(default=0),
        ),
    ]