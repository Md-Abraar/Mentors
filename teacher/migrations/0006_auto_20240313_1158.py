# Generated by Django 3.0.14 on 2024-03-13 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0005_examiner_mentor_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examiner',
            name='mentor_image',
        ),
        migrations.AddField(
            model_name='examiner',
            name='examiner_image',
            field=models.ImageField(default=6, upload_to='Faculty/'),
            preserve_default=False,
        ),
    ]
