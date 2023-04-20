# import os

from django.contrib import admin
from . import questionsFileProgram as q_prog
# from django.core.exceptions import ValidationError
# from django.http import HttpResponse, FileResponse, HttpResponseRedirect
# from django.urls import reverse
# from django.utils.html import format_html

from .models import Question, Chapter, File


# Register the admin class with the associated model
class FileAdmin(admin.ModelAdmin):
    model = File

    def save_model(self, request, obj, form, change):
        # Call the parent class's save_model method to save the uploaded file
        super().save_model(request, obj, form, change)
        if obj.type_switch == 'q':
            # Open the uploaded file and read the data
            file_path = obj.file.path

            a,b,c,d=q_prog.do_a_list(file_path)
            num_of_chapters=len(a)
            iter_val=0
            for i in range(0,num_of_chapters):
                # First we check for similar question entries
                tmp_arr=[]
                tmp_qst=Question.objects.filter(title=a[i]).first()
                if tmp_qst is None:
                    tmp_ch = int(d[i])
                    for ii in range(iter_val, tmp_ch):
                        # Then we check for the similar chapter entries
                        tmp_ch_obj = Chapter.objects.filter(description=c[ii]).first()
                        if tmp_ch_obj is None:
                            print(c[ii])
                            ch_obj = Chapter(description=c[ii])
                            ch_obj.save()
                        ch_mtm=Chapter.objects.get(description=c[ii])
                        tmp_arr.append(ch_mtm)
                    qst_obj=Question(title=a[i],question=b[i])
                    qst_obj.save()
                    qst_obj.chapters.set(tmp_arr)
                    iter_val += (tmp_ch-iter_val)-1

    list_display = ('id','title', 'file')


admin.site.register(File, FileAdmin)


class ChapterAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Call the parent class's save_model method to save the uploaded file
        desc_lower = obj.description.lower()
        # Check for similar entries based on case-insensitive search
        similar_chapters = Chapter.objects.filter(description__iexact=desc_lower).exclude(pk=obj.pk)

        # If similar entries are found, raise a validation error
        if similar_chapters.exists():
            message = 'Similar entries already exist in the database.'
            self.message_user(request, message, level='warning')
            return

        # Save the model instance
        super().save_model(request, obj, form, change)


admin.site.register(Chapter, ChapterAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'display_chapters')


admin.site.register(Question, QuestionAdmin)
