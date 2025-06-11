from django.urls import path
from . import views

urlpatterns = [
    path('tasks/',views.TaskListView.as_view(),name='tasks'),
    path('task_create/',views.TaskCreateView.as_view(),name='create_task'),
    path('task_update/<int:pk>/',views.TaskUpdateView.as_view(),name='task_update'),
    path('task_delete/<int:pk>/',views.TaskDeleteView.as_view(),name='task_delete'),
]
