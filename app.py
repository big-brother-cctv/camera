import cv2
from flask import Flask, Response

app = Flask(__name__)

CAMERA_SOURCE = 0

camera = cv2.VideoCapture(CAMERA_SOURCE)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not camera.isOpened():
    print("❌ ERROR: Camera not found")
else:
    print("✅ Camera found")

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        # Redimensionar el frame por si acaso
        frame = cv2.resize(frame, (640, 480))

        # Codificar a JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
