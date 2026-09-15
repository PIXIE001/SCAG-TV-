"""
SCAG LIVE TV
VIRTUAL STUDIO COMPOSITOR
"""

from pathlib import Path
import cv2
import numpy as np


class SCAGCompositor:

    WIDTH = 1920
    HEIGHT = 1080

    def studio_canvas(
        self,
        scene="main"
    ):

        canvas = np.zeros(
            (
                self.HEIGHT,
                self.WIDTH,
                3
            ),
            dtype=np.uint8
        )

        # Navy foundation
        canvas[:, :] = (
            24,
            35,
            82
        )

        # Large central screen
        cv2.rectangle(
            canvas,
            (390, 100),
            (1530, 650),
            (35, 65, 115),
            -1
        )

        # Screen frame
        cv2.rectangle(
            canvas,
            (390, 100),
            (1530, 650),
            (180, 215, 240),
            5
        )

        cv2.putText(
            canvas,
            "SCAG LIVE TV",
            (600, 280),
            cv2.FONT_HERSHEY_SIMPLEX,
            2.2,
            (255, 255, 255),
            5
        )

        cv2.putText(
            canvas,
            "NEWS",
            (810, 390),
            cv2.FONT_HERSHEY_SIMPLEX,
            2.0,
            (180, 220, 255),
            4
        )

        cv2.putText(
            canvas,
            "DETERMINED TO EXCEL",
            (700, 510),
            cv2.FONT_HERSHEY_SIMPLEX,
            .85,
            (255, 255, 255),
            2
        )

        # Desk
        if scene == "main":

            cv2.rectangle(
                canvas,
                (250, 730),
                (1670, 1040),
                (28, 35, 50),
                -1
            )

            cv2.rectangle(
                canvas,
                (250, 730),
                (1670, 1040),
                (170, 205, 225),
                4
            )

            # Chair 1
            cv2.rectangle(
                canvas,
                (390, 620),
                (650, 900),
                (10, 15, 25),
                -1
            )

            # Chair 2
            cv2.rectangle(
                canvas,
                (1270, 620),
                (1530, 900),
                (10, 15, 25),
                -1
            )

        return canvas

    def place_presenter(
        self,
        studio,
        presenter_rgba,
        x,
        y,
        width
    ):

        if presenter_rgba is None:

            return studio

        original_h, original_w = (
            presenter_rgba.shape[:2]
        )

        ratio = width / original_w

        height = int(
            original_h * ratio
        )

        presenter = cv2.resize(
            presenter_rgba,
            (width, height)
        )

        x2 = min(
            studio.shape[1],
            x + width
        )

        y2 = min(
            studio.shape[0],
            y + height
        )

        crop_w = x2 - x
        crop_h = y2 - y

        if crop_w <= 0 or crop_h <= 0:

            return studio

        presenter = presenter[
            :crop_h,
            :crop_w
        ]

        alpha = (
            presenter[:, :, 3:4]
            .astype(np.float32)
            / 255.0
        )

        foreground = (
            presenter[:, :, :3]
            .astype(np.float32)
        )

        background = (
            studio[
                y:y2,
                x:x2
            ].astype(np.float32)
        )

        result = (
            foreground * alpha
            +
            background * (1 - alpha)
        )

        studio[
            y:y2,
            x:x2
        ] = result.astype(
            np.uint8
        )

        return studio
