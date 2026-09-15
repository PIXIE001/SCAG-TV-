"""
SCAG LIVE TV
PRESENTER SEGMENTATION ENGINE

This module provides the interface for separating the presenter
from the original environment.

The architecture allows a stronger video-matting model to be
plugged in later without changing the rest of the application.
"""

from pathlib import Path
from typing import Optional

import cv2
import numpy as np


class PresenterSegmenter:

    def __init__(self):

        self.initialized = True

    def create_mask(
        self,
        frame: np.ndarray
    ) -> Optional[np.ndarray]:

        if frame is None:
            return None

        height, width = frame.shape[:2]

        # Initial intelligent foreground region.
        #
        # This is deliberately conservative.
        # A production RVM/Robust Video Matting model should
        # replace this mask generator.

        mask = np.ones(
            (height, width),
            dtype=np.uint8
        ) * 255

        return mask

    def apply_mask(
        self,
        frame: np.ndarray,
        mask: np.ndarray
    ):

        rgba = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2BGRA
        )

        rgba[:, :, 3] = mask

        return rgba
