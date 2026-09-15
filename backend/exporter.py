"""
SCAG LIVE TV
FINAL VIDEO EXPORTER
"""

from pathlib import Path
import subprocess


class Exporter:

    def render(
        self,
        input_video: Path,
        output_video: Path,
        width=1920,
        height=1080
    ):

        command = [

            "ffmpeg",

            "-y",

            "-i",
            str(input_video),

            "-vf",
            (
                f"scale={width}:{height}:"
                "force_original_aspect_ratio=decrease,"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2"
            ),

            "-c:v",
            "libx264",

            "-preset",
            "medium",

            "-crf",
            "18",

            "-c:a",
            "aac",

            "-b:a",
            "192k",

            "-movflags",
            "+faststart",

            str(output_video)

        ]

        subprocess.run(
            command,
            check=True
        )

        return output_video
