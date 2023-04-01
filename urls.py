from django.urls import path
from . import views
#from django.urls.conf import url


urlpatterns = [
    path(r'^$', views.index, name='index'),
    path('chapters/', views.ChapterListView.as_view(), name='chapters'),
    path('questions/', views.QuestionListView.as_view(), name='questions'),
    path('script/', views.ScriptListView, name='script'),
    path(r'chapter/<str:description>/', views.ChapterDetailView.as_view(), name='chapter-detail'),
path(r'questin/<str:title>/', views.QuestionDetailView.as_view(), name='question-detail'),
]