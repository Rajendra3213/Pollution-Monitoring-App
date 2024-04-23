# Generated by Django 5.0.4 on 2024-04-23 21:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomUser', '0017_alter_emailconfirm_time_valid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailconfirm',
            name='time_valid',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 23, 21, 56, 56, 997169, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='treeplantation',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='treeplantation',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
