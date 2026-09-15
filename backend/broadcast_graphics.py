"""
SCAG LIVE TV
BROADCAST GRAPHICS
"""

import cv2


class BroadcastGraphics:

    def headline(
        self,
        frame,
        text
    ):

        if not text:
            return frame

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (0, 0),
            (frame.shape[1], 105),
            (5, 15, 45),
            -1
        )

        frame = cv2.addWeighted(
            overlay,
            .88,
            frame,
            .12,
            0
        )

        cv2.putText(
            frame,
            text,
            (45, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        return frame

    def lower_third(
        self,
        frame,
        text
    ):

        if not text:
            return frame

        h, w = frame.shape[:2]

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (45, h - 160),
            (w - 45, h - 65),
            (10, 25, 65),
            -1
        )

        frame = cv2.addWeighted(
            overlay,
            .90,
            frame,
            .10,
            0
        )

        cv2.putText(
            frame,
            text,
            (75, h - 95),
            cv2.FONT_HERSHEY_SIMPLEX,
            .95,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        return frame

    def watermark(
        self,
        frame
    ):

        h, w = frame.shape[:2]

        cv2.putText(
            frame,
            "SCAG LIVE TV",
            (w - 280, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            .75,
            (220, 220, 220),
            2,
            cv2.LINE_AA
        )

        return frame
