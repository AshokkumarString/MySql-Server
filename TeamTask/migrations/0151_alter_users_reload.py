# Generated by Django 3.2.9 on 2022-02-23 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamTask', '0150_users_reload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='reload',
            field=models.BooleanField(default=False),
        ),
    ]
