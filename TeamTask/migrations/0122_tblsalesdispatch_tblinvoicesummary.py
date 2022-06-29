# Generated by Django 3.2.9 on 2022-01-25 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0121_tblstock_hsncode'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblsalesdispatch',
            name='tblinvoicesummary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tblinvoicesummary', to='TeamTask.tblinvoicesummary'),
        ),
    ]