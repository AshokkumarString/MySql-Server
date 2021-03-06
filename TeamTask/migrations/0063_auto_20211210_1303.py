# Generated by Django 3.2.5 on 2021-12-10 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0062_tblbatch_tbllocation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tbllocation',
            old_name='buildingno',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='tbllocation',
            old_name='country',
            new_name='location',
        ),
        migrations.RenameField(
            model_name='tbllocation',
            old_name='district',
            new_name='shortlocation',
        ),
        migrations.RemoveField(
            model_name='tbllocation',
            name='postcode',
        ),
        migrations.RemoveField(
            model_name='tbllocation',
            name='state',
        ),
        migrations.AlterField(
            model_name='tblbatch',
            name='batchno',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
