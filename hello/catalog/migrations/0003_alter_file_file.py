# Generated by Django 4.2 on 2023-04-04 16:36

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_file_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\alban\\OneDrive\\Bureau\\project\\locallibrary'), upload_to=''),
        ),
    ]
