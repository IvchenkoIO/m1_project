
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import generic
import os
from .models import Question,Chapter
import questionsFileProgram as qa

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
class ChapterDetailView(generic.DetailView):
    model = Question
    context_object_name = 'question-list'
    template_name = 'catalog/book_list_chapter.html'

    def get_object(self, queryset=None):
        # Get the description field value from the URL
        description = self.kwargs.get('description')

        # Retrieve the Chapter object with the matching description field value
        queryset = self.get_queryset()
        queryset = queryset.filter(description__iexact=description)

        # Return the Chapter object or raise a 404 error if not found
        try:
            chapter = ChapterListView.queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("Chapter does not exist")

        return chapter

    def get_context_data(self, **kwargs):
        context = super(ChapterDetailView, self).get_context_data(**kwargs)
        _chosen_chapter = self.kwargs['description']
        # do something with book_id and book_title
        return context
#def index(request):
  #  return HttpResponse(simple_func())


##To complete
class QuestionDetailView(generic.DetailView):
    model = Question
    context_object_name = 'question-list'
    template_name = 'catalog/book_list_chapter.html'

    def get_object(self, queryset=None):
        # Get the description field value from the URL
        title = self.kwargs.get('title')

        # Retrieve the Chapter object with the matching description field value
        queryset = self.get_queryset()
        queryset = queryset.filter(title__iexact=title)

        # Return the Chapter object or raise a 404 error if not found
        try:
            chapter = ChapterListView.queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("Question does not exist")

        return chapter

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        _chosen_chapter = self.kwargs['title']
        # do something with book_id and book_title
        return context


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