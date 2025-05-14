# استخدم بيئة رسمية لدعم Poetry
FROM python:3.10

# إعداد بيئة العمل
WORKDIR /app

# نسخ ملفات Poetry
COPY pyproject.toml poetry.lock ./

# تثبيت Poetry
RUN pip install poetry

# تثبيت التبعيات
RUN poetry install

# نسخ بقية الملفات
COPY . .

# تدريب Rasa
RUN poetry run rasa train

# تشغيل Rasa عند الإقلاع
CMD ["poetry", "run", "rasa", "run", "--enable-api", "--cors", "*", "--port", "5005"]
