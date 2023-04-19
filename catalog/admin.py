from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html

from .models import Question,Chapter,File

# Register the admin class with the associated model
class MyModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Call the parent class's save_model method to save the uploaded file
        super().save_model(request, obj, form, change)

        # Open the uploaded file and read the data
        file_path = obj.file.path
        with open(file_path, 'r') as f:
            for line in f:
                # Create a new MyModel object for each row in the CSV file
                mymodel_obj = Question()
                mymodel_obj.title = line
                # Set other fields as needed
                mymodel_obj.save()


admin.site.register(File,MyModelAdmin)
admin.site.register(Course)
admin.site.register(Chapter)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
       list_display = ('title', 'display_chapters')