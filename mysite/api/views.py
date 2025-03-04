from django.shortcuts import render
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer

# 📌 Lấy danh sách tất cả task + Thêm mới
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
# 📌 Lấy 1 task theo ID + Cập nhật + Xóa
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer