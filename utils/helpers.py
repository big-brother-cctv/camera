"""
helpers.py

Utility functions for image processing.
"""

import cv2

def rotate_frame(frame, angle):
    """
    Rotates a frame by the specified angle.

    Args:
        frame (numpy.ndarray): The image frame to rotate.
        angle (int): The rotation angle (0, 90, 180, 270).

    Returns:
        numpy.ndarray: The rotated frame.
    """
    if angle == 90:
        return cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        return cv2.rotate(frame, cv2.ROTATE_180)
    elif angle == 270:
        return cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return frame
