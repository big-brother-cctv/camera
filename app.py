import os
import time
import requests
import subprocess

CONFIG_URL = os.getenv("CONFIG_URL", "http://api:8080/api/cameras/1")

print(f"Fetching camera config from {CONFIG_URL}...")
try:
    config = requests.get(CONFIG_URL).json()
except Exception as e:
    print(f"Failed to fetch config: {e}")
    exit(1)

camera_device = config.get("cameraDevice", "/dev/video0")
resolution = config.get("resolution", "640x480")
framerate = str(config.get("framerate", 25))
rtsp_url = config.get("rtspUrl", "rtsp://mediamtx.default.svc.cluster.local:8554/mystream")
video_codec = config.get("videoCodec", "libx264")
preset = config.get("preset", "ultrafast")
tune = config.get("tune", "zerolatency")
buffer_size = str(config.get("bufferSize", "1000000"))
rotate = int(config.get("rotate", 0))

print(f"Waiting for {camera_device}...")
while not os.path.exists(camera_device):
    time.sleep(1)

rotate_filter = ""
if rotate == 90:
    rotate_filter = "-vf transpose=1"
elif rotate == 180:
    rotate_filter = "-vf transpose=2,transpose=2"
elif rotate == 270:
    rotate_filter = "-vf transpose=2"

cmd = [
    "ffmpeg", "-f", "v4l2", "-framerate", framerate, "-video_size", resolution,
    "-i", camera_device, "-vcodec", video_codec, "-preset", preset, "-tune", tune
]

if rotate_filter:
    cmd.extend(rotate_filter.split())

cmd += ["-f", "rtsp", "-rtsp_transport", "tcp", "-buffer_size", buffer_size, rtsp_url]

print(f"Starting stream to {rtsp_url}")
subprocess.run(cmd)
