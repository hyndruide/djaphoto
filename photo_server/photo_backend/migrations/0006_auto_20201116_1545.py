# Generated by Django 3.1.3 on 2020-11-16 14:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('photo_backend', '0005_auto_20201116_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='date_create',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
