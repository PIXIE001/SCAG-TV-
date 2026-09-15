"""
SCAG LIVE TV
VIDEO PROCESSING ENGINE
"""

from pathlib import Path
import subprocess
import shutil


class VideoProcessor:

    def __init__(self):

        self.ffmpeg = shutil.which("ffmpeg")

        if not self.ffmpeg:
            raise RuntimeError(
                "FFmpeg is required for video processing."
            )

    def probe(self, video: Path):

        command = [
            self.ffmpeg.replace(
                "ffmpeg",
                "ffprobe"
            ),
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(video)
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        return result.stdout

    def convert(
        self,
        input_video: Path,
        output_video: Path
    ):

        command = [
            self.ffmpeg,
            "-y",
            "-i",
            str(input_video),

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

    def preserve_audio(
        self,
        original_video: Path,
        processed_video: Path,
        final_video: Path
    ):

        command = [
            self.ffmpeg,
            "-y",

            "-i",
            str(processed_video),

            "-i",
            str(original_video),

            "-map",
            "0:v:0",

            "-map",
            "1:a:0?",

            "-c:v",
            "copy",

            "-c:a",
            "aac",

            "-b:a",
            "192k",

            "-shortest",

            str(final_video)
        ]

        subprocess.run(
            command,
            check=True
        )

        return final_video
