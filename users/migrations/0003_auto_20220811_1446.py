# Generated by Django 3.2.15 on 2022-08-11 06:46

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_doctor'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Doctor',
        ),
        migrations.DeleteModel(
            name='Patient',
        ),
        migrations.CreateModel(
            name='DoctorUser',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
        ),
        migrations.CreateModel(
            name='PatientUser',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('patient_id', models.AutoField(primary_key=True, serialize=False)),
                ('patient_name', models.CharField(max_length=100)),
                ('patient_dob', models.DateField()),
                ('patient_address', models.TextField(blank=True)),
                ('patient_contact', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(regex='^\\+?\\d{9,16}$')])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
