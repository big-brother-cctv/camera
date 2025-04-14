import cv2
import time
from flask import Flask, Response

app = Flask(__name__)

CAMERA_SOURCE = 0
camera = cv2.VideoCapture(CAMERA_SOURCE)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_FPS, 30)
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

if not camera.isOpened():
    print("❌ ERROR: Camera not found")
else:
    print("✅ Camera found")

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        # frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR)

        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if not ret:
            continue

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        time.sleep(0.03)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
