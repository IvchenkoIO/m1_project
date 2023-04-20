import random
import unicodedata
import urllib

from django.http import HttpResponse  # Http404
# import hello.ai as ai
from django.shortcuts import render, get_object_or_404
from django.views import generic
import os
from easylearn import settings
from .models import Question, Chapter, File
# import hello.questionsFileProgram as qa
from . import js_script as cm


# from . import apps as app


def index(request):
    """
    Display function for the home page of the site.
    """
    # Generation of "quantities" of some main objects
    num_questions = Question.objects.all().count()
    num_chapters = Chapter.objects.all().count()
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


class ChapterListView(generic.ListView):
    model = Chapter
    paginate_by = 10
    context_object_name = 'chapter_list'  # your own context variable name in the template

    def get_queryset(self):
        return Chapter.objects.filter(description__icontains="")  # Get Chapter entries

    template_name = 'catalog/chapter_list.html'  # Determine your template name and location



class QuestionListView(generic.ListView):
    model = Question
    paginate_by = 10
    context_object_name = 'question_list'  # your own context variable name in the template

    def get_queryset(self):
        return Question.objects.filter(title__icontains="")  # Get Question entries

    template_name = 'catalog/question_list.html'  # Determine your template name and location



# To get the list of questions based on chapter
def ChapterQuizView(request, description):
    # Retrieve all Chapter objects from the database
    chapters = Chapter.objects.all()

    # Retrieve the Chapter object with the matching description field value
    try:
        chapter = get_object_or_404(Chapter, description__iexact=description)
        questions = Question.objects.filter(chapters__description__in=['' + chapter.description + ''])
        count = questions.count()
        qlist = []
        if count < 10:
            qlist = list(questions)
        else:
            for i in range(0, 10):
                rand = random.randint(0, count)
                qlist.insert(i, questions[rand])
        cm.make_conv(qlist)
        context = {
            'question_list': qlist,
            'chapter_list': chapters
        }
        return render(request, 'catalog/quiz.html', context)
    except Chapter.MultipleObjectsReturned:
        context = {
            'error': "Returned too many matching entries, contact your teacher to review it!",
        }
        return render(request, 'catalog/error.html', context)


def QuestionDetailView(request, title):
    # Retrieve the Question object with the matching description field value
    question = get_object_or_404(Question, title__iexact=title)
    context = {
        'question': question
    }
    return render(request, 'catalog/question_detail.html', context)


def FileDownloader(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            # Normalize the file name using NFKD normalization
            normalized_file_name = unicodedata.normalize('NFKD', file_name)
            # Encode the file name using UTF-8 with URL encoding
            encoded_file_name = urllib.parse.quote(normalized_file_name.encode('utf-8'))
            response['Content-Disposition'] = f'attachment; filename="{encoded_file_name}"'
            return response
    else:
        return HttpResponse('File not found')


