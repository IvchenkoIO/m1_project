from django.db import models
from django.urls import reverse
import uuid
from django.core.files.storage import FileSystemStorage
# Create your models here.

class Course(models.Model):
    title=models.TextField(max_length=500,help_text="Write the title of the course",default='')
    description=models.TextField(max_length=100,default='',help_text='Short description of the course')
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


class Chapter(models.Model):
    title=models.TextField(max_length=500,help_text="Write the title of the chapter",default='')
    description=models.TextField(max_length=100,default='',help_text='Short description of the chapter')
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
    title=models.TextField(max_length=500, help_text="Write a short description",default='')
    question=models.TextField(max_length=500)
    POINTS=(
        ('0','too bad'),
        ('1','bad'),
        ('2','not that bad'),
        ('3','ok'),
        ('4','good'),
        ('5','perfect'),

    )
    answer_points=models.CharField(max_length=1,choices=POINTS,default='0')
    chapters=models.ManyToManyField(Chapter,help_text="Select chapters that explains this question ")
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
    fs=FileSystemStorage(location="C:\\Users\\alban\\OneDrive\\Bureau\\project\\locallibrary")
    title = models.CharField(max_length=50)
    file = models.FileField(storage=fs)
