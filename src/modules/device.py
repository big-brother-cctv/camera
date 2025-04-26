"""
Device utilities for camera application.
"""

import os
import time

def wait_for_device(device):
    """
    Wait until the specified device file exists.

    Args:
        device (str): Device file path.
    """
    print(f"Waiting for {device}...")
    while not os.path.exists(device):
        time.sleep(1)
