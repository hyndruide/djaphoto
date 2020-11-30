# Generated by Django 3.1.3 on 2020-11-30 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_backend', '0002_photo-sync-api'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paillasson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=255)),
                ('code_connexion', models.CharField(max_length=255)),
                ('is_valid', models.BooleanField(default=False)),
            ],
        ),
    ]
