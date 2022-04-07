# Generated by Django 4.0.3 on 2022-04-07 12:50

from django.db import migrations, models
import resolutions.models


class Migration(migrations.Migration):

    dependencies = [
        ('resolutions', '0002_alter_certificate_options_alter_resolution_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='certificateimage',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='resolution',
            options={'ordering': ['number']},
        ),
        migrations.AddField(
            model_name='certificate',
            name='is_minutes_of_meeting',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='certificateimage',
            name='image',
            field=models.ImageField(upload_to=resolutions.models.CertificateImage.certificate_image_path),
        ),
    ]