# Generated by Django 4.1.7 on 2023-04-19 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearn', '0006_remove_file_my_switch_file_type_switch'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='title',
            field=models.TextField(default='', help_text='The name of the chapter', max_length=100),
        ),
    ]
