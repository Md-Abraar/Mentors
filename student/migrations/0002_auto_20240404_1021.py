# Generated by Django 3.0.14 on 2024-04-04 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personal_details',
            name='student_id',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
