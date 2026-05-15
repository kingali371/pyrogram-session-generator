FROM python:3.10-slim

WORKDIR /app

# تثبيت المتطلبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود
COPY src/ ./src/
COPY tests/ ./tests/
COPY run.py .

# تشغيل الاختبارات
CMD ["pytest", "tests/", "-v"]
