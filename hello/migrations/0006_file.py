# Generated by Django 4.1.7 on 2023-03-29 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0005_rename_chapters_chapter_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='')),
            ],
        ),
    ]