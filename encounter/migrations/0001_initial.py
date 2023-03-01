# Generated by Django 3.2.15 on 2022-09-12 04:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appointment', '0003_auto_20220822_1140'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0007_auto_20220814_2306'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encounter',
            fields=[
                ('encounter_id', models.AutoField(primary_key=True, serialize=False)),
                ('encounter_date', models.DateField()),
                ('encounter_time', models.TimeField()),
                ('encounter_appointment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='encounter_appointment', to='appointment.appointment')),
                ('encounter_created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='encounter_created_by', to=settings.AUTH_USER_MODEL)),
                ('encounter_doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='encounter_doctor', to='users.doctor')),
                ('encounter_patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='encounter_patient', to='users.patient')),
            ],
        ),
    ]