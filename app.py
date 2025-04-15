import os
import cv2
import time
from flask import Flask, Response

app = Flask(__name__)

# Configurable camera parameters via environment variables
CAMERA_SOURCE = int(os.getenv("CAMERA_SOURCE", 0))
FRAME_WIDTH = int(os.getenv("FRAME_WIDTH", 640))
FRAME_HEIGHT = int(os.getenv("FRAME_HEIGHT", 480))
FRAME_RATE = int(os.getenv("FRAME_RATE", 30))
JPEG_QUALITY = int(os.getenv("JPEG_QUALITY", 80))
FOURCC = os.getenv("FOURCC", "MJPG")
SLEEP_TIME = float(os.getenv("SLEEP_TIME", 0.03))
ROTATE = int(os.getenv("ROTATE", 0))  # 0, 90, 180, 270 degrees

camera = cv2.VideoCapture(CAMERA_SOURCE)

# Apply settings
camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
camera.set(cv2.CAP_PROP_FPS, FRAME_RATE)
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*FOURCC))

def rotate_frame(frame, angle):
    if angle == 90:
        return cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        return cv2.rotate(frame, cv2.ROTATE_180)
    elif angle == 270:
        return cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return frame 

if not camera.isOpened():
    print("❌ ERROR: Camera not found")
else:
    print("✅ Camera found")

def generate_frames():
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

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
