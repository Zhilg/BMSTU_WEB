# Generated by Django 4.2 on 2023-09-09 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0003_userprofiles_has_module_perms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofiles',
            name='has_module_perms',
        ),
    ]
