# Generated by Django 4.0.3 on 2023-05-26 17:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdffile',
            name='pdf',
            field=models.FileField(upload_to='pdf/', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
    ]
