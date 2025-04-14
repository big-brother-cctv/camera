FROM python:3.11-bullseye

RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt --no-cache-dir --prefer-binary

EXPOSE 5000

CMD ["python", "app.py"]
