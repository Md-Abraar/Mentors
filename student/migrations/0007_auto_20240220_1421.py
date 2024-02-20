# Generated by Django 3.0.14 on 2024-02-20 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mentor', '0002_mentor_mentor_image'),
        ('student', '0006_auto_20240215_1010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='TD',
        ),
        migrations.RemoveField(
            model_name='student',
            name='address',
        ),
        migrations.RemoveField(
            model_name='student',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='student',
            name='profile_pic',
        ),
        migrations.AddField(
            model_name='student',
            name='mentor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mentor.mentor'),
        ),
    ]
