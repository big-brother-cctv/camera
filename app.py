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

device = config.get("device", "/dev/video0")
resolution = config.get("resolution", "640x480")
fps = str(config.get("fps", 25))
postUrl = config.get("postUrl", "rtsp://mediamtx.default.svc.cluster.local:8554/mystream")
codec = config.get("codec", "libx264")
preset = config.get("preset", "ultrafast")
tune = config.get("tune", "zerolatency")
buffer = str(config.get("buffer", "1000000"))
rotation = int(config.get("rotation", 0))

print(f"Waiting for {device}...")
while not os.path.exists(device):
    time.sleep(1)

rotate_filter = ""
if rotation == 90:
    rotate_filter = "-vf transpose=1"
elif rotation == 180:
    rotate_filter = "-vf transpose=2,transpose=2"
elif rotation == 270:
    rotate_filter = "-vf transpose=2"

cmd = [
    "ffmpeg", "-f", "v4l2", "-framerate", fps, "-video_size", resolution,
    "-i", device, "-vcodec", codec, "-preset", preset, "-tune", tune
]

if rotate_filter:
    cmd.extend(rotate_filter.split())

cmd += ["-f", "rtsp", "-rtsp_transport", "tcp", "-buffer_size", buffer, postUrl]

print(f"Starting stream to {postUrl}")
subprocess.run(cmd)
