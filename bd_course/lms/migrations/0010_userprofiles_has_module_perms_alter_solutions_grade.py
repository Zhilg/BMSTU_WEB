# Generated by Django 4.2 on 2023-09-23 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0009_alter_solutions_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofiles',
            name='has_module_perms',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='solutions',
            name='grade',
            field=models.IntegerField(default=-1),
        ),
    ]
