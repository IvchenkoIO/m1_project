from django.urls import path
# from django.views.static import serve

from . import views

# from django.urls.conf import url


urlpatterns = [
    path('', views.index, name='index'),
    path('chapters/', views.ChapterListView.as_view(), name='chapters'),
    path('questions/', views.QuestionListView.as_view(), name='questions'),
    path('chapter/<str:description>/', views.ChapterQuizView, name='chapter-detail'),
    path('question/<str:title>/', views.QuestionDetailView, name='question-detail'),
    path('files/<str:file_name>/', views.FileDownloader, name='download_file'),
]
