import pyaudio
import whisper
import numpy as np
import soundfile as sf
import time

# Cấu hình âm thanh
# Cấu hình âm thanh
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024  # Kích thước nhỏ để ghi âm mượt mà
RECORD_DURATION = 5  # Ghi âm 10 giây (có thể thay đổi)

# Tải mô hình Whisper (chỉ tải một lần khi server khởi động)
model = whisper.load_model("small")

# Hàm xử lý speech-to-text (ghi âm trong thời gian cố định)
def speech_to_text_whisper_def():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    print(f"Đang ghi âm {RECORD_DURATION} giây...")
    
    # Tính số khung cần ghi
    frames_to_record = int(RATE / CHUNK * RECORD_DURATION)
    audio_frames = []
    
    # Ghi âm trong RECORD_DURATION giây
    for _ in range(frames_to_record):
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_frames.append(data)
    
    print("Đã ghi âm xong! Đang xử lý...")
    
    # Chuyển dữ liệu thành mảng numpy
    audio_data = b''.join(audio_frames)
    audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
    
    # Lưu thành file wav
    sf.write("recorded.wav", audio_array, RATE)
    
    # Xử lý với Whisper
    start_time = time.time()
    result = model.transcribe("recorded.wav", language="vi")
    text = result["text"]
    
    # In kết quả (cho debug)
    if text:
        print(f"Văn bản (xử lý trong {time.time() - start_time:.2f}s): {text}")
    else:
        print("Không nhận diện được gì.")
    
    # Đóng stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    return text

# Chạy
if __name__ == "__main__":
    try:
        speech_to_text_whisper_def()
    except KeyboardInterrupt:
        print("\nĐã dừng!")