# Generated by Django 3.0.14 on 2024-04-06 04:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
        ('examiner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(default='', max_length=50)),
                ('course_name', models.CharField(max_length=50)),
                ('question_number', models.PositiveIntegerField(blank=True, null=True)),
                ('total_marks', models.PositiveIntegerField(blank=True, null=True)),
                ('passcode', models.CharField(blank=True, max_length=50, null=True)),
                ('examiner_id', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty_id', models.CharField(max_length=10)),
                ('faculty_name', models.CharField(max_length=30)),
                ('faculty_branch', models.CharField(max_length=30)),
                ('faculty_designation', models.CharField(max_length=25)),
                ('faculty_email', models.EmailField(max_length=254)),
                ('faculty_phone', models.CharField(max_length=10)),
                ('faculty_image', models.ImageField(upload_to='static/Faculty/')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('skill_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('sector', models.CharField(max_length=30)),
                ('domain', models.CharField(max_length=50)),
                ('level', models.CharField(max_length=15)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='students_skills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=30)),
                ('test_score', models.IntegerField(blank=True, null=True)),
                ('project_name', models.CharField(blank=True, max_length=50, null=True)),
                ('project_type', models.CharField(blank=True, max_length=50, null=True)),
                ('project_score', models.IntegerField(blank=True, null=True)),
                ('certification_status', models.BooleanField(default=False)),
                ('updated_date', models.DateField(blank=True, null=True)),
                ('skill_status', models.CharField(default='pending', max_length=20)),
                ('overall_score', models.IntegerField(blank=True, null=True)),
                ('assessed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='examiner.Examiner')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.Student')),
            ],
        ),
        migrations.CreateModel(
            name='student_skill_exam_applications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sem', models.IntegerField(blank=True, null=True)),
                ('branch', models.CharField(max_length=30)),
                ('section', models.CharField(max_length=30)),
                ('mentor_identity_number', models.CharField(max_length=30)),
                ('requested_date', models.DateField(blank=True, null=True)),
                ('completed_date', models.DateField(blank=True, null=True)),
                ('application_status', models.CharField(default='pending', max_length=30)),
                ('skill_name', models.CharField(max_length=30)),
                ('assessed_by', models.CharField(max_length=30)),
                ('exam_id', models.CharField(blank=True, max_length=30, null=True)),
                ('marks_obtained', models.CharField(blank=True, max_length=30, null=True)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.PositiveIntegerField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.PositiveIntegerField(blank=True, null=True)),
                ('question', models.CharField(max_length=600)),
                ('option1', models.CharField(max_length=200)),
                ('option2', models.CharField(max_length=200)),
                ('option3', models.CharField(max_length=200)),
                ('option4', models.CharField(max_length=200)),
                ('answer', models.CharField(choices=[('Option1', 'Option1'), ('Option2', 'Option2'), ('Option3', 'Option3'), ('Option4', 'Option4')], max_length=200)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.Course')),
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
        migrations.CreateModel(
            name='examiner_skills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=30)),
                ('skill_status', models.CharField(default=False, max_length=20)),
                ('examiner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='examiner.Examiner')),
            ],
        ),
    ]