from django.urls import path
from .views import TaskListCreateView, TaskDetailView, ask_ai, ask_ai_json, analyze_image, text_to_speech, speech_to_text, speech_to_text_whisper # Import đúng tên class

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('ask-ai', ask_ai, name='ask-ai'),
    path('ask-ai-json', ask_ai_json, name='ask-ai-json'),
    path('analyze-image', analyze_image, name='analyze-image'),
    path('text-to-speech', text_to_speech, name='text-to-speech'),
    path('speech-to-text', speech_to_text, name='speech-to-text'),
    path('speech-to-text-whisper', speech_to_text_whisper, name='speech-to-text-whisper')
]