# Generated by Django 4.2 on 2023-09-09 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofiles',
            name='has_module_perms',
            field=models.BooleanField(default=False),
        ),
    ]
