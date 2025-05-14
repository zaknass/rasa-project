FROM python:3.9

WORKDIR /app

# نسخ requirements فقط وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ كل ملفات المشروع
COPY . .

# تدريب نموذج Rasa
RUN rasa run actions

# إعلام Render أن البورت المفتوح هو 5005
EXPOSE 5055

# تشغيل السيرفر
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5055"]
