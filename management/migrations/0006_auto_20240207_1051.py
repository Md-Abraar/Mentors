# Generated by Django 3.0.14 on 2024-02-07 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0005_auto_20201209_2125'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty_id', models.CharField(max_length=10)),
                ('faculty_name', models.CharField(max_length=30)),
                ('faculty_branch', models.CharField(max_length=30)),
                ('faculty_email', models.EmailField(max_length=254)),
                ('faculty_phone', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('skill_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('domain', models.CharField(max_length=50)),
                ('sub_domain', models.CharField(max_length=50)),
                ('level', models.CharField(max_length=15)),
                ('parameters', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Mentorship',
            fields=[
                ('mentor_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('faculty_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.Faculty')),
            ],
        ),
        migrations.AddField(
            model_name='faculty',
            name='skill_set',
            field=models.ManyToManyField(to='management.Skill'),
        ),
    ]
