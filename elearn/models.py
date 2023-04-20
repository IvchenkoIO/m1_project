import os

from django.db import models
# from django import forms
from django.urls import reverse
# import uuid
from django.core.files.storage import FileSystemStorage
# Create your models here.
from easylearn import settings
from . import apps as app


class Chapter(models.Model):
    objects = models.Manager()
    MultipleObjectsReturned = None
    description=models.TextField(max_length=100, default='', help_text='Short description of the chapter')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.description

    def get_absolute_url(self):
        """
        Returns the url to access a particular question instance.
        """
        return reverse('chapter-detail', args=[str(self.description)])


class Question(models.Model):
    objects = models.Manager()
    title=models.TextField(max_length=500, help_text="Write a short description",default='')
    question=models.TextField(max_length=500)
    chapters=models.ManyToManyField(Chapter,help_text="Selelct chapters that explains this question ")

    # Admin panel visualization
    def display_chapters(self):
        """
        """
        return ', '.join([Chapter.description for Chapter in self.chapters.all()[:3]])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular question instance.
        """
        return reverse('question-detail', args=[str(self.title)])


class File(models.Model):
    objects = models.Manager()
    location=os.path.join(settings.BASE_DIR,app.ELearnConfig.name,'files' )
    fs=FileSystemStorage(location=location)
    title = models.CharField(max_length=50)
    SWITCH_CHOICES = (
        ('q', 'Question list'),  # Display 'Question list' for True
        ('l', 'Lectures'),  # Display 'Lectures' for False
    )
    type_switch = models.CharField(
        max_length=3,
        choices=SWITCH_CHOICES,
        default='on',  # Set the default value of the field
        verbose_name="File type"
    )
    file = models.FileField(storage=fs)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

    def download(self):
        """
        Returns the url to access a particular question instance.
        """
        file_name = self.file.name
        return reverse('download_file', args=[str(file_name)])
