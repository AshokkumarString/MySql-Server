# Generated by Django 3.2.9 on 2022-02-22 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0149_users_purchase'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='reload',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
