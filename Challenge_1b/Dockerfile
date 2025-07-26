FROM python:3.10-slim

# Install system dependencies including Tesseract
RUN apt-get update && \
    apt-get install -y tesseract-ocr poppler-utils && \
    apt-get clean

WORKDIR /app

COPY Challenge_1a Challenge_1a
COPY Challenge_1b Challenge_1b

WORKDIR /app/Challenge_1b

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python3", "run_processor.py"]
