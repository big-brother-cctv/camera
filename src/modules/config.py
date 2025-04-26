"""
Configuration utilities for camera application.
"""

import os
import requests

CAMERA_NAME = os.getenv("CAMERA_NAME", "default-camera")
API_URL = os.getenv("API_URL", f"http://localhost:8080/api")
INTERNAL_TOKEN = os.getenv("INTERNAL_TOKEN", "internal-token-dev")
MEDIAMTX_URL = os.getenv("MEDIAMTX_URL", "rtsp://mediamtx.local")
POLL_INTERVAL = int(os.getenv("CONFIG_POLL_INTERVAL", 10))

def register_camera(default_config):
    """
    Register a camera with the default configuration.

    Args:
        default_config (dict): Default camera configuration.
    """
    headers = {"Authorization": f"Bearer {INTERNAL_TOKEN}"}
    try:
        resp = requests.post(f"{API_URL}/cameras", json=default_config, headers=headers)
        if resp.status_code == 201:
            print(f"Camera '{CAMERA_NAME}' registered with default config.")
        else:
            print(f"Failed to register camera: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"Exception during camera registration: {e}")

def fetch_config(camera_name):
    """
    Fetch the configuration for a given camera.

    Args:
        camera_name (str): Name of the camera.

    Returns:
        dict or None: Camera configuration or None if not found.
    """
    config_url = f"{API_URL}/cameras/search?name={camera_name}"
    headers = {"Authorization": f"Bearer {INTERNAL_TOKEN}"}
    try:
        resp = requests.get(config_url, headers=headers)
        configs = resp.json()
        if not configs:
            print(f"No config found for camera name '{camera_name}'")
            return None
        config = configs[0]
    except Exception as e:
        print(f"Failed to fetch config: {e}")
        return None
    return config

def configs_equal(a, b):
    """
    Compare two camera configurations for equality.

    Args:
        a (dict): First configuration.
        b (dict): Second configuration.

    Returns:
        bool: True if configurations are equal, False otherwise.
    """
    keys = ["device", "resolution", "fps", "postUrl", "codec", "preset", "tune", "buffer", "rotation"]
    return all(a.get(k) == b.get(k) for k in keys)
