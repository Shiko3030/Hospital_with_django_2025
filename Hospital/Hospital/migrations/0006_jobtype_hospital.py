# Generated by Django 5.0.6 on 2025-04-14 00:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0005_alter_patient_national_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobtype',
            name='hospital',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Hospital.hospital'),
        ),
    ]
