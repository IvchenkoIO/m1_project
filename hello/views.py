import random

from django.http import HttpResponse, Http404
#import hello.ai as ai
from django.shortcuts import render, get_object_or_404
from django.views import generic
import os
from easylearn import settings
from .models import Question,Chapter,File
#import hello.questionsFileProgram as qa

def index(request):
    """
    Display function for the home page of the site.
    """

    # Generation of "quantities" of some main objects
    num_questions=Question.objects.all().count()
    num_chapters=Chapter.objects.all().count()
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_questions': num_questions, 'num_chapters': num_chapters,
                 'num_visits': num_visits},  # num_visits appended
    )
    # Render the HTML template index.html with data inside context variable

class ChapterListView(generic.ListView):
    model = Chapter
    paginate_by = 10
    context_object_name = 'chapter_list'  # your own context variable name in the template
    def get_queryset(self):
        return Chapter.objects.filter(description__icontains="") # Get 5 books containing
    template_name = 'catalog/chapter_list.html'  # Determine your template name and location

    def get_context_data(self, **kwargs):
        # First of all, we get the basic implementation of the context
        context = super(ChapterListView, self).get_context_data(**kwargs)
        # Add a new variable to the context and initialize it with some value
        context['some_data'] = 'This is just some data'
        return context

class QuestionListView(generic.ListView):
    model = Question
    paginate_by = 10
    context_object_name = 'question_list'  # your own context variable name in the template
    def get_queryset(self):
        return Question.objects.filter(title__icontains="") # Get 5 books containing
    template_name = 'catalog/question_list.html'  # Determine your template name and location

    def get_context_data(self, **kwargs):
        # First of all, we get the basic implementation of the context
        context = super(QuestionListView, self).get_context_data(**kwargs)
        # Add a new variable to the context and initialize it with some value
        context['some_data'] = 'This is just some data'
        return context

##To get the list of questions based on chapter
##To complete
def ChapterQuizView(request, description):
    # Retrieve the Chapter object with the matching description field value
    chapter = get_object_or_404(Chapter, description__iexact=description)

    # Fetch all questions that have a ManyToMany relationship with the selected chapter
    questions = Question.objects.filter(chapters__description__in=[''+chapter.description+''])
    count=questions.count()
    qlist=[]
    if count<10:
        qlist=list(questions)
    else:
        for i in range (0,10):
            rand=random.randint(0,count)
            qlist.insert(i,questions[rand])
    context = {
        'question_list': qlist
    }
    return render(request, 'catalog/question_list_chapter.html',context)
##To complete
def QuestionDetailView(request, title):
        # Retrieve the Chapter object with the matching description field value
    question = get_object_or_404(Question, title__iexact=title)

        # Fetch all questions that have a ManyToMany relationship with the selected chapter
        #questions = Question.objects.filter(chapters__description__in=['' + chapter.description + ''])

    context = {
           'question': question
    }

    return render(request, 'catalog/test3.html')


def FileDownloader(request,file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    else:
        return HttpResponse('File not found')




'''
##Define script run
def ScriptListView(generic):
    # Код для выполнения скрипта здесь
    file_content = "Hello, world!"
    file_name = "example.txt"
    data=qa.do_a_list()
    with open(file_name, "w") as f:
        for i in range(0,len(data)):
            f.write(data[i])
            q=Question(title=data[i])
            q.save()
        #f.write(file_content)

    # Get the file size for the Content-Length header
    file_size = os.path.getsize(file_name)

    # Create an HTTP response with the file as the content
    response = HttpResponse(open(file_name, "rb").read(), content_type="text/plain")
    response["Content-Disposition"] = f"attachment; filename={file_name}"
    response["Content-Length"] = file_size
    return response
'''