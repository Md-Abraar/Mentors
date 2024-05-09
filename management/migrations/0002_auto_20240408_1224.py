# Generated by Django 3.0.14 on 2024-04-08 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examiner_skills',
            name='skill_name',
        ),
        migrations.AddField(
            model_name='examiner_skills',
            name='skill_name',
            field=models.ManyToManyField(to='management.Skill'),
        ),
    ]
