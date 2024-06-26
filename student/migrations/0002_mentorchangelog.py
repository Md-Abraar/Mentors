# Generated by Django 3.0.14 on 2024-04-15 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MentorChangeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('emp_id', models.CharField(max_length=40)),
                ('men_name', models.CharField(max_length=50)),
                ('department', models.CharField(max_length=40)),
                ('branch', models.CharField(max_length=6)),
                ('stu_roll', models.CharField(max_length=40)),
                ('stu_name', models.CharField(max_length=40)),
                ('stu_sem', models.IntegerField()),
                ('stu_sec', models.CharField(max_length=1)),
                ('stu_score', models.IntegerField()),
            ],
        ),
    ]
