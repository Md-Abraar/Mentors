# Generated by Django 3.0.14 on 2024-04-10 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievements',
            name='achieve_file',
            field=models.FileField(blank=True, null=True, upload_to='static/students_files/'),
        ),
    ]
