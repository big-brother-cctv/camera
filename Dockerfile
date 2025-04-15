FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    v4l-utils \
    && rm -rf /var/lib/apt/lists/*

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]