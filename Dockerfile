FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY app.py .

RUN pip install --no-cache-dir flask opencv-python

EXPOSE 5000

CMD ["python", "app.py"]