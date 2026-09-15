"""
SCAG LIVE TV
VIRTUAL STUDIO ENGINE
"""

from pathlib import Path

import cv2
import numpy as np


class StudioEngine:

    def __init__(self):

        self.width = 1920
        self.height = 1080

    def create_background(
        self,
        scene: str
    ):

        canvas = np.zeros(
            (
                self.height,
                self.width,
                3
            ),
            dtype=np.uint8
        )

        # Navy studio base

        canvas[:, :] = (
            20,
            30,
            70
        )

        # Studio horizontal lighting

        for y in range(0, self.height, 80):

            cv2.line(
                canvas,
                (0, y),
                (self.width, y),
                (35, 90, 140),
                2
            )

        # Central screen

        screen_x1 = 420
        screen_y1 = 120

        screen_x2 = 1500
        screen_y2 = 650

        cv2.rectangle(
            canvas,
            (screen_x1, screen_y1),
            (screen_x2, screen_y2),
            (35, 55, 105),
            -1
        )

        # Studio screen border

        cv2.rectangle(
            canvas,
            (screen_x1, screen_y1),
            (screen_x2, screen_y2),
            (170, 210, 240),
            5
        )

        # Station branding

        cv2.putText(
            canvas,
            "SCAG LIVE TV",
            (610, 270),
            cv2.FONT_HERSHEY_SIMPLEX,
            2.4,
            (255, 255, 255),
            5,
            cv2.LINE_AA
        )

        cv2.putText(
            canvas,
            "NEWS",
            (790, 370),
            cv2.FONT_HERSHEY_SIMPLEX,
            2.0,
            (180, 220, 255),
            4,
            cv2.LINE_AA
        )

        cv2.putText(
            canvas,
            "Senior Chief Adano Girls Senior School",
            (515, 470),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        cv2.putText(
            canvas,
            "DETERMINED TO EXCEL",
            (690, 540),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (210, 210, 210),
            2,
            cv2.LINE_AA
        )

        if scene == "main":

            cv2.rectangle(
                canvas,
                (300, 720),
                (1620, 1020),
                (35, 40, 55),
                -1
            )

            cv2.rectangle(
                canvas,
                (300, 720),
                (1620, 1020),
                (170, 200, 220),
                5
            )

            cv2.putText(
                canvas,
                "SCAG LIVE TV",
                (720, 870),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (255, 255, 255),
                3,
                cv2.LINE_AA
            )

        return canvas

    def resize_for_output(
        self,
        frame
    ):

        return cv2.resize(
            frame,
            (
                self.width,
                self.height
            )
        )
