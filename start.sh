#!/bin/bash

echo "Waiting for /dev/video0..."
while [ ! -e /dev/video0 ]; do sleep 1; done

RTSP_URL=${RTSP_URL:-rtsp://mediamtx.default.svc.cluster.local:8554/mystream}

echo "Starting stream in $RTSP_URL"

ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 \
  -vcodec libx264 -preset ultrafast -tune zerolatency \
  -f rtsp "$RTSP_URL"
