# Generated by Django 4.2 on 2023-04-04 15:32

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='', help_text='Short description of the chapter', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\alban\\OneDrive\\Bureau\\m1_project'), upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='', help_text='Write a short description', max_length=500)),
                ('question', models.TextField(max_length=500)),
                ('answer_points', models.CharField(choices=[('0', 'too bad'), ('1', 'bad'), ('2', 'not that bad'), ('3', 'ok'), ('4', 'good'), ('5', 'perfect')], default='0', max_length=1)),
                ('chapters', models.ManyToManyField(help_text='Selelct chapters that explains this question ', to='catalog.chapter')),
            ],
        ),
    ]