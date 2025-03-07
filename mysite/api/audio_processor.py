import pyaudio
from vosk import Model, KaldiRecognizer
import json

class AudioProcessor:
    def __init__(self, model_path="/Users/nguyenhuuloc/Downloads/hackathon/mysite/vosk-model-vn-0.4", rate=16000, chunk=1024):
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, rate)
        self.chunk = chunk
        self.rate = rate
        self.format = pyaudio.paInt16
        self.channels = 1
        self.audio = pyaudio.PyAudio()

    def process_audio(self):
        """Xử lý âm thanh từ micro và chuyển thành văn bản."""
        stream = self.audio.open(format=self.format,
                                 channels=self.channels,
                                 rate=self.rate,
                                 input=True,
                                 frames_per_buffer=self.chunk)
        print("🎤 Đang nghe... (Nhấn Ctrl+C để dừng)")
        
        try:
            while True:
                data = stream.read(self.chunk, exception_on_overflow=False)
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "")
                    if text:
                        print("✅ Kết quả cuối: ", text)
                else:
                    partial_result = json.loads(self.recognizer.PartialResult())
                    partial_text = partial_result.get("partial", "")
                    if partial_text:
                        print("\r🔄 Real-time: " + partial_text, end="", flush=True)
        except KeyboardInterrupt:
            print("\n🔴 Đã dừng!")
        finally:
            stream.stop_stream()
            stream.close()
            self.audio.terminate()

if __name__ == "__main__":
    processor = AudioProcessor()
    processor.process_audio()