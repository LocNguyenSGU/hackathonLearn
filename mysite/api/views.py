from django.shortcuts import render
from django.http import JsonResponse
import openai
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from dotenv import load_dotenv
import os


# 📌 Lấy danh sách tất cả task + Thêm mới
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
# 📌 Lấy 1 task theo ID + Cập nhật + Xóa
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key="")


def ask_ai(request):
    question = request.GET.get("question", "Xin chào!")  # Lấy câu hỏi từ request (nếu không có thì mặc định là "Xin chào!")

    try:
        # 📌 Gọi API OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role": "user", "content": question}],
        )

        # 📌 Lấy nội dung phản hồi từ API
        answer = response.choices[0].message.content.strip()
        return JsonResponse({"response": answer}, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)  # Bắt lỗi nếu có vấn đề