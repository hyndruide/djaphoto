# Generated by Django 3.1.3 on 2020-11-22 08:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('photo_backend', '0002_auto_20201116_1124'), ('photo_backend', '0003_photo_photobooth'), ('photo_backend', '0004_photobooth_sessionkey'), ('photo_backend', '0005_auto_20201116_1526'), ('photo_backend', '0006_auto_20201116_1545'), ('photo_backend', '0007_auto_20201116_1547'), ('photo_backend', '0008_auto_20201119_0845')]

    dependencies = [
        ('photo_backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photobooth',
            options={'verbose_name': 'Photo Booth'},
        ),
        migrations.AddField(
            model_name='photo',
            name='photobooth',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='photo_backend.photobooth'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photobooth',
            name='sessionkey',
            field=models.CharField(default='9ebbd0b25760557393a43064a92bae539d962103', max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_create',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_create',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_create',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='date_upload',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_create',
            field=models.DateTimeField(),
        ),
    ]