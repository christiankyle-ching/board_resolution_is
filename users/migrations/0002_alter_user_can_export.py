# Generated by Django 4.0.4 on 2022-05-05 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='can_export',
            field=models.BooleanField(default=False, help_text='Enables PDF exporting for this user.'),
        ),
    ]
