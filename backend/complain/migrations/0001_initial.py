# Generated by Django 5.0.4 on 2024-04-26 07:09

import complain.models
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ValidationAuthority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('name', models.CharField(max_length=100)),
                ('contact', models.CharField(blank=True, max_length=14, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+977'. Up to 10 digits allowed.", regex='^(\\+977)?\\d{9,10}$')])),
            ],
            options={
                'verbose_name': 'ValidationAuthority',
                'verbose_name_plural': 'ValidationAuthority List',
            },
        ),
        migrations.CreateModel(
            name='UserComplain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('image', models.ImageField(upload_to=complain.models.get_complain_image_upload_path)),
                ('description', models.TextField()),
                ('severity_level', models.CharField(choices=[('very_minimum', 'Very Minimum'), ('low', 'Low'), ('high', 'High'), ('very_high', 'Very High')], max_length=20)),
                ('solved', models.BooleanField(default=False)),
                ('date_of_complain', models.DateTimeField(auto_now_add=True)),
                ('solved_date', models.DateTimeField()),
                ('complain_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('validated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='complain.validationauthority')),
            ],
        ),
    ]
