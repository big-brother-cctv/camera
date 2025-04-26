import os
import time
import copy
import subprocess

from modules.config import (
    fetch_config, register_camera, configs_equal,
    CAMERA_NAME, API_URL, INTERNAL_TOKEN,
    MEDIAMTX_URL, POLL_INTERVAL
)
from modules.ffmpeg import build_cmd, run_ffmpeg
from modules.device import wait_for_device

def main():
    last_config = None
    ffmpeg_proc = None

    default_config = {
        "name": CAMERA_NAME,
        "device": "/dev/video0",
        "resolution": "640x480",
        "fps": 25,
        "codec": "libx264",
        "preset": "ultrafast",
        "tune": "zerolatency",
        "buffer": "1000000",
        "rotation": 0
    }

    while True:
        config = fetch_config(CAMERA_NAME)
        if not config:
            print("No config found, registering camera with default config...")
            register_camera(default_config)
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
            if ffmpeg_proc and ffmpeg_proc.poll() is not None:
                print("ffmpeg exited unexpectedly, restarting...")
                cmd, device, postUrl = build_cmd(config)
                wait_for_device(device)
                ffmpeg_proc = run_ffmpeg(cmd)

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
