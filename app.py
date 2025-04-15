"""
app.py

Flask application that serves the video stream.
"""

from flask import Flask, Response
from camera.stream import generate_frames
from config.settings import PORT

app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    """
    HTTP endpoint that returns a multipart MJPEG video stream.

    Returns:
        Response: Flask streaming response.
    """
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
