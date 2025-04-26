"""
FFmpeg command utilities for camera streaming.
"""

import subprocess
from modules.config import CAMERA_NAME, MEDIAMTX_URL

def build_cmd(config):
    """
    Build the ffmpeg command based on camera configuration.

    Args:
        config (dict): Camera configuration.

    Returns:
        tuple: (command list, device path, postUrl)
    """
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

def run_ffmpeg(cmd):
    """
    Start the ffmpeg process.

    Args:
        cmd (list): FFmpeg command.

    Returns:
        subprocess.Popen: The running process.
    """
    print(f"Starting stream: {' '.join(cmd)}")
    return subprocess.Popen(cmd)
