"""
SCAG LIVE TV
PRESENTER ANALYZER
"""

from pathlib import Path
import cv2


class PresenterAnalyzer:

    def analyze(
        self,
        video_path: Path
    ):

        capture = cv2.VideoCapture(
            str(video_path)
        )

        if not capture.isOpened():

            raise RuntimeError(
                "Cannot open presenter video."
            )

        width = int(
            capture.get(
                cv2.CAP_PROP_FRAME_WIDTH
            )
        )

        height = int(
            capture.get(
                cv2.CAP_PROP_FRAME_HEIGHT
            )
        )

        fps = capture.get(
            cv2.CAP_PROP_FPS
        )

        frames = int(
            capture.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )

        duration = (
            frames / fps
            if fps
            else 0
        )

        capture.release()

        if width > height:

            orientation = "landscape"

        else:

            orientation = "portrait"

        return {

            "width":
                width,

            "height":
                height,

            "fps":
                fps,

            "frames":
                frames,

            "duration":
                duration,

            "orientation":
                orientation,

            "movement_preservation":
                True,

            "original_voice":
                True,

            "original_clothing":
                True,

            "original_expression":
                True

        }
