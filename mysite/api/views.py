from django.shortcuts import render
from django.http import JsonResponse
import openai
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
    
# 🔥 Cách mới để gọi OpenAI API
# client = openai.OpenAI(api_key="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")

client = openai.OpenAI(api_key="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")


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