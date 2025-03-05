from django.urls import path
from .views import TaskListCreateView, TaskDetailView, ask_ai  # Import đúng tên class

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('ask-ai', ask_ai, name='ask-ai'),
]