# Generated by Django 3.0.14 on 2024-02-28 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentor', '0007_auto_20240227_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
