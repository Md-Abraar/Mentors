# Generated by Django 3.0.14 on 2024-04-08 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20240408_1224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examiner_skills',
            name='skill_status',
        ),
    ]
