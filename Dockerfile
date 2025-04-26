FROM debian:bullseye-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    v4l-utils \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY src .
CMD ["python3", "app.py"]
