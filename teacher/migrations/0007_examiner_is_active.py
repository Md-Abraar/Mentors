# Generated by Django 3.0.14 on 2024-03-16 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0006_auto_20240313_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='examiner',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]