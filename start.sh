#!/bin/bash

CAMERA_DEVICE="${CAMERA_DEVICE:-/dev/video0}"
RESOLUTION="${RESOLUTION:-640x480}"
FRAMERATE="${FRAMERATE:-25}"
RTSP_URL="${RTSP_URL:-rtsp://mediamtx.default.svc.cluster.local:8554/mystream}"
VIDEO_CODEC="${VIDEO_CODEC:-libx264}"
PRESET="${PRESET:-ultrafast}"
TUNE="${TUNE:-zerolatency}"
BUFFER_SIZE="${BUFFER_SIZE:-1000000}"
ROTATE="${ROTATE:-0}"

echo "Waiting for $CAMERA_DEVICE..."
while [ ! -e "$CAMERA_DEVICE" ]; do sleep 1; done

echo "Streaming $CAMERA_DEVICE in $RTSP_URL with resolution $RESOLUTION and $FRAMERATE fps"

# Camera rotation
case "$ROTATE" in
  90)
    ROTATE_FILTER="-vf transpose=1"  # 90º
    ;;
  180)
    ROTATE_FILTER="-vf transpose=2,transpose=2"  # 180º
    ;;
  270)
    ROTATE_FILTER="-vf transpose=2"  # 270º
    ;;
  *)
    ROTATE_FILTER=""
    ;;
esac

ffmpeg -f v4l2 -framerate "$FRAMERATE" -video_size "$RESOLUTION" -i "$CAMERA_DEVICE" \
  -vcodec "$VIDEO_CODEC" -preset "$PRESET" -tune "$TUNE" \
  $ROTATE_FILTER \
  -f rtsp -rtsp_transport tcp -buffer_size "$BUFFER_SIZE" "$RTSP_URL"
