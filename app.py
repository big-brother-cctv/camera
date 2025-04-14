import cv2
from flask import Flask, Response

app = Flask(__name__)

CAMERA_SOURCE = 0

camera = cv2.VideoCapture(CAMERA_SOURCE)

if not camera.isOpened():
    print("❌ ERROR: Camera not found")
else:
    print("✅ Camera found")

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '<h1>Cam Stream</h1><img src="/video_feed">'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
