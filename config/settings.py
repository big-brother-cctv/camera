"""
settings.py

Configuration settings loaded from environment variables.
"""

import os

# Camera configuration
CAMERA_SOURCE = int(os.getenv("CAMERA_SOURCE", 0))
FRAME_WIDTH = int(os.getenv("FRAME_WIDTH", 640))
FRAME_HEIGHT = int(os.getenv("FRAME_HEIGHT", 480))
FRAME_RATE = int(os.getenv("FRAME_RATE", 30))
JPEG_QUALITY = int(os.getenv("JPEG_QUALITY", 80))
FOURCC = os.getenv("FOURCC", "MJPG")
SLEEP_TIME = float(os.getenv("SLEEP_TIME", 0.03))
ROTATE = int(os.getenv("ROTATE", 0))  # Rotation: 0, 90, 180, or 270 degrees

# Flask server
PORT = int(os.getenv("PORT", 5000))
