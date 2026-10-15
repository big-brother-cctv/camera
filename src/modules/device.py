"""
Device utilities for camera application.
"""

import os
import time

def wait_for_device(device, source_type="v4l2"):
    """
    Wait until the specified device exists.
    Only blocks for local hardware devices (e.g. /dev/video0).
    Network streams (RTSP, HTTP) or synthetic test feeds are skipped immediately.
    """
    if source_type in ("rtsp", "http", "mjpeg", "test") or (device and not device.startswith("/dev/")):
        return

    print(f"Waiting for hardware device {device}...")
    while not os.path.exists(device):
        time.sleep(1)
