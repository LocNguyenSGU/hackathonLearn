import json
from django.shortcuts import render
from django.http import JsonResponse
import openai
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from django.views.decorators.csrf import csrf_exempt
from .audio_processor import AudioProcessor
from .whisper import speech_to_text_whisper_def


# 📌 Lấy danh sách tất cả task + Thêm mới
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
# 📌 Lấy 1 task theo ID + Cập nhật + Xóa
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    

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
@csrf_exempt 
def ask_ai_json(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        # 🔹 Lấy dữ liệu JSON từ request
        data = json.loads(request.body)
        question = data.get("question", "Xin chào!")  # Lấy câu hỏi từ request JSON

        # 📌 Gửi yêu cầu đến OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role": "user", "content": question}],
            max_tokens=300,  # 🔹 Giới hạn số token trong phản hồi (~225-250 từ)
        )

        # 📌 Lấy nội dung phản hồi từ API
        answer = response.choices[0].message.content.strip()

        return JsonResponse({"response": answer}, json_dumps_params={'ensure_ascii': False})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt  # 🟢 Bỏ qua kiểm tra CSRF
def analyze_image(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        # 🟡 Đọc dữ liệu JSON từ request
        data = json.loads(request.body)
        image_url = data.get("image_url")  # 🟠 Lấy URL ảnh từ request
        question = data.get("question", "What's in this image?")  # 🟣 Lấy câu hỏi (mặc định)

        if not image_url:
            return JsonResponse({"error": "Missing image_url"}, status=400)

        # 🟡 Gửi yêu cầu đến OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 🔵 Chọn model GPT-4o-mini
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},  # 🟣 Nội dung câu hỏi
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,  # 🟠 URL ảnh từ request
                                "detail": "high",  # 🔴 Yêu cầu phân tích chi tiết
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,  # 🔵 Giới hạn số token phản hồi (~225-250 từ)
        )

        # 🟢 Lấy kết quả phản hồi từ API
        answer = response.choices[0].message.content.strip()
        return JsonResponse({"response": answer}, json_dumps_params={'ensure_ascii': False})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt  # 🟢 Bỏ qua kiểm tra CSRF
def text_to_speech(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        # 🟡 Lấy dữ liệu JSON từ request
        data = json.loads(request.body)
        text = data.get("text")  # 🟠 Lấy văn bản cần chuyển thành giọng nói
        print(text)

        if not text:
            return JsonResponse({"error": "Missing 'text' field"}, status=400)

        # 🟡 Gửi yêu cầu đến OpenAI TTS API
        response = client.audio.speech.create(
            model="tts-1",   # 🔵 Chọn model TTS của OpenAI
            voice="alloy",   # 🟣 Chọn giọng đọc (có thể đổi: "nova", "shimmer", "echo", v.v.)
            input=text,      # 🟠 Văn bản cần chuyển đổi
        )

        # 🟢 Lưu file giọng nói dưới dạng .mp3
        file_path = "output.mp3"
        response.stream_to_file(file_path)

        # 🟢 Trả về file âm thanh cho người dùng
        return FileResponse(open(file_path, "rb"), content_type="audio/mpeg")

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
def speech_to_text(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        processor = AudioProcessor()  # Khởi tạo đối tượng xử lý âm thanh
        text = processor.process_audio()  # Gọi phương thức xử lý

        return JsonResponse({"text": text}, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
# API endpoint
@csrf_exempt
def speech_to_text_whisper(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=400)
    
    try:
        text = speech_to_text_whisper_def()  # Ghi âm 10 giây và trả về kết quả
        return JsonResponse({"text": text}, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)