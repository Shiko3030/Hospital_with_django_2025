# Generated by Django 5.0.6 on 2025-04-14 00:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0006_jobtype_hospital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobtype',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hospital.hospital'),
        ),
    ]
