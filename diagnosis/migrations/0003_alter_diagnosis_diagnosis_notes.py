# Generated by Django 3.2.15 on 2022-09-15 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosis', '0002_auto_20220915_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnosis',
            name='diagnosis_notes',
            field=models.JSONField(default=dict),
        ),
    ]