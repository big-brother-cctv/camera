#!/bin/bash

CAMERA_DEVICE="${CAMERA_DEVICE:-/dev/video0}"
RESOLUTION="${RESOLUTION:-640x480}"
FRAMERATE="${FRAMERATE:-25}"
RTSP_URL="${RTSP_URL:-rtsp://mediamtx.default.svc.cluster.local:8554/mystream}"
VIDEO_CODEC="${VIDEO_CODEC:-libx264}"
PRESET="${PRESET:-ultrafast}"
TUNE="${TUNE:-zerolatency}"

echo "Waiting for $CAMERA_DEVICE..."
while [ ! -e "$CAMERA_DEVICE" ]; do sleep 1; done

echo "Streaming $CAMERA_DEVICE in $RTSP_URL with resolution $RESOLUTION and $FRAMERATE fps"

ffmpeg -re -f v4l2 -framerate "$FRAMERATE" -video_size "$RESOLUTION" -i "$CAMERA_DEVICE" \
  -vcodec "$VIDEO_CODEC" -preset "$PRESET" -tune "$TUNE" \
  -f rtsp "$RTSP_URL"

