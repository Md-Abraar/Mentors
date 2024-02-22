# Generated by Django 3.0.14 on 2024-02-20 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_teacher_skill'),
        ('quiz', '0015_auto_20240220_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students_skills',
            name='assessed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='teacher.Teacher'),
        ),
    ]
