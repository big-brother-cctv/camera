import os
import time
import requests
import subprocess
import signal
import copy

CAMERA_NAME = os.getenv("CAMERA_NAME", "default-camera")
API_URL = os.getenv("API_URL", f"http://localhost:8080/api/cameras")
MEDIAMTX_URL = os.getenv("MEDIAMTX_URL", "rtsp://mediamtx.local")
INTERNAL_TOKEN = os.getenv("INTERNAL_TOKEN", "internal-token-dev")
POLL_INTERVAL = int(os.getenv("CONFIG_POLL_INTERVAL", 10))

config_url = f"{API_URL}/search?name={CAMERA_NAME}"

def fetch_config():
    headers = {"Authorization": f"Bearer {INTERNAL_TOKEN}"}
    try:
        resp = requests.get(config_url, headers=headers)
        configs = resp.json()
        if not configs:
            print(f"No config found for camera name '{CAMERA_NAME}'")
            return None
        config = configs[0]
    except Exception as e:
        print(f"Failed to fetch config: {e}")
        return None
    return config

def build_cmd(config):
    device = config.get("device", "/dev/video0")
    resolution = config.get("resolution", "640x480")
    fps = str(config.get("fps", 25))
    postUrl = f"{MEDIAMTX_URL}/{CAMERA_NAME}"
    codec = config.get("codec", "libx264")
    preset = config.get("preset", "ultrafast")
    tune = config.get("tune", "zerolatency")
    buffer = str(config.get("buffer", "1000000"))
    rotation = int(config.get("rotation", 0))

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
    return cmd, device, postUrl

def configs_equal(a, b):
    # Compare only relevant keys
    keys = ["device", "resolution", "fps", "postUrl", "codec", "preset", "tune", "buffer", "rotation"]
    return all(a.get(k) == b.get(k) for k in keys)

def wait_for_device(device):
    print(f"Waiting for {device}...")
    while not os.path.exists(device):
        time.sleep(1)

def run_ffmpeg(cmd):
    print(f"Starting stream: {' '.join(cmd)}")
    return subprocess.Popen(cmd)

def main():
    last_config = None
    ffmpeg_proc = None

    while True:
        config = fetch_config()
        if not config:
            print("Retrying config fetch in 5 seconds...")
            time.sleep(5)
            continue

        if last_config is None or not configs_equal(config, last_config):
            if ffmpeg_proc:
                print("Config changed, restarting ffmpeg...")
                ffmpeg_proc.terminate()
                try:
                    ffmpeg_proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    ffmpeg_proc.kill()
            cmd, device, postUrl = build_cmd(config)
            wait_for_device(device)
            ffmpeg_proc = run_ffmpeg(cmd)
            last_config = copy.deepcopy(config)
        else:
            # Check if ffmpeg died unexpectedly
            if ffmpeg_proc and ffmpeg_proc.poll() is not None:
                print("ffmpeg exited unexpectedly, restarting...")
                cmd, device, postUrl = build_cmd(config)
                wait_for_device(device)
                ffmpeg_proc = run_ffmpeg(cmd)

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
