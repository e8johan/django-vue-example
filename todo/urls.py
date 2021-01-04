from django.urls import path

from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.index, name='index'),
    
    path('api/todo', views.api_todo_list),
    path('api/todo/<int:todo_id>/', views.api_todo_details),
]
