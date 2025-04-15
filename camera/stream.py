"""
stream.py

Handles camera initialization and frame generation.
"""

import cv2
import time
from config.settings import (
    CAMERA_SOURCE, FRAME_WIDTH, FRAME_HEIGHT, FRAME_RATE,
    FOURCC, JPEG_QUALITY, SLEEP_TIME, ROTATE
)
from utils.helpers import rotate_frame

# Initialize the camera
camera = cv2.VideoCapture(CAMERA_SOURCE)

# Apply camera settings
camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
camera.set(cv2.CAP_PROP_FPS, FRAME_RATE)
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*FOURCC))

if not camera.isOpened():
    print("❌ ERROR: Camera not found")
else:
    print("✅ Camera found")

def generate_frames():
    """
    Generator function that yields JPEG-encoded video frames.

    Yields:
        bytes: A multipart JPEG frame formatted for streaming.
    """
    while True:
        success, frame = camera.read()
        if not success:
            break

        frame = rotate_frame(frame, ROTATE)

        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])
        if not ret:
            continue

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        time.sleep(SLEEP_TIME)
