"""
FFmpeg command utilities for all types of cameras (V4L2, IP RTSP, HTTP, Synthetic Test).
"""

import subprocess
from modules.config import CAMERA_NAME, MEDIAMTX_URL

def build_cmd(config):
    """
    Build the ffmpeg command based on camera configuration.
    Supports:
      - Local hardware USB/V4L2 cameras (/dev/video*)
      - Remote IP cameras (RTSP, RTMP, HTTP MJPEG)
      - Synthetic Test feed (simulated camera for development/testing)

    Args:
        config (dict): Camera configuration.

    Returns:
        tuple: (command list, device path, postUrl, source_type)
    """
    source_type = config.get("sourceType", "v4l2")
    source_url = config.get("sourceUrl", "")
    device = config.get("device", "/dev/video0")
    resolution = config.get("resolution", "640x480")
    fps = str(config.get("fps", 30))
    camera_name = config.get("name", CAMERA_NAME)
    postUrl = f"{MEDIAMTX_URL}/{camera_name}"
    codec = config.get("codec", "libx264")
    preset = config.get("preset", "ultrafast")
    tune = config.get("tune", "zerolatency")
    buffer = str(config.get("buffer", "1000000"))
    rotation = int(config.get("rotation", 0))

    # Auto-detect source_type if not specified
    if not source_type or source_type == "v4l2":
        if (source_url and source_url.startswith("rtsp://")) or (device and device.startswith("rtsp://")):
            source_type = "rtsp"
        elif (source_url and source_url.startswith("http")) or (device and device.startswith("http")):
            source_type = "http"
        elif device in ("test", "virtual") or source_url in ("test", "virtual"):
            source_type = "test"
        else:
            source_type = "v4l2"

    rotate_filter = ""
    if rotation == 90:
        rotate_filter = "-vf transpose=1"
    elif rotation == 180:
        rotate_filter = "-vf transpose=2,transpose=2"
    elif rotation == 270:
        rotate_filter = "-vf transpose=2"

    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "warning"]

    # 1. Synthetic Test camera (No hardware needed)
    if source_type == "test":
        cmd += [
            "-re", "-f", "lavfi",
            "-i", f"testsrc=size={resolution}:rate={fps}",
            "-vcodec", "libx264", "-pix_fmt", "yuv420p", "-preset", preset, "-tune", tune
        ]

    # 2. IP Camera over RTSP
    elif source_type == "rtsp":
        ip_url = source_url or device
        cmd += [
            "-rtsp_transport", "tcp",
            "-i", ip_url
        ]
        # Si no hay rotación, podemos re-codificar en ultralow latency o copiar stream
        if rotate_filter:
            cmd += ["-vcodec", codec, "-preset", preset, "-tune", tune]
        else:
            cmd += ["-vcodec", "copy"]

    # 3. IP Camera over HTTP / MJPEG
    elif source_type in ("http", "mjpeg"):
        ip_url = source_url or device
        cmd += [
            "-i", ip_url,
            "-vcodec", codec, "-preset", preset, "-tune", tune
        ]

    # 4. Local USB / V4L2 webcam
    else:
        cmd += [
            "-f", "v4l2", "-framerate", fps, "-video_size", resolution,
            "-i", device,
            "-vcodec", codec, "-preset", preset, "-tune", tune
        ]

    if rotate_filter and source_type != "test":
        cmd.extend(rotate_filter.split())

    cmd += [
        "-f", "rtsp", "-rtsp_transport", "tcp",
        "-buffer_size", buffer,
        postUrl
    ]

    target_source = source_url if source_url else device
    return cmd, target_source, postUrl, source_type

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
