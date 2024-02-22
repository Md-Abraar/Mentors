# Generated by Django 3.0.14 on 2024-02-13 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_auto_20240213_1135'),
        ('quiz', '0010_auto_20240212_2110'),
    ]

    operations = [
        migrations.CreateModel(
            name='teacher_skills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=30)),
                ('skill_status', models.CharField(default='pending', max_length=20)),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='teacher.Teacher')),
            ],
        ),
    ]
