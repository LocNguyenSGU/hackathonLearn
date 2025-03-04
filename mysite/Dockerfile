# Sử dụng Python 3 chính thức
FROM python:3.11

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements.txt vào container
COPY requirements.txt requirements.txt

# Cài đặt thư viện
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ source code vào container
COPY . .

# Chạy migrate (để tạo database nếu có)
RUN python manage.py migrate

# Chạy server Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]