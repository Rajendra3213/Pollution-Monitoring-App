# Generated by Django 5.0.4 on 2024-04-23 20:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomUser', '0015_alter_emailconfirm_time_valid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailconfirm',
            name='time_valid',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 23, 21, 12, 29, 686747, tzinfo=datetime.timezone.utc)),
        ),
    ]