"""
SCAG LIVE TV
ROBUST VIDEO MATTING ENGINE

Purpose:
Separate the original presenter from the original environment
while preserving the presenter's real movement and appearance.
"""

from pathlib import Path
import subprocess
import shutil
import torch


class RVMEngine:

    def __init__(self):

        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.model = None

    def load_model(self):

        if self.model is not None:
            return

        # Official Robust Video Matting TorchHub model.
        self.model = torch.hub.load(
            "PeterL1n/RobustVideoMatting",
            "mobilenetv3"
        )

        self.model = self.model.eval()

        if self.device == "cuda":
            self.model = self.model.cuda()

    def check_gpu(self):

        return {
            "cuda_available":
                torch.cuda.is_available(),

            "device":
                self.device,

            "gpu_name":
                (
                    torch.cuda.get_device_name(0)
                    if torch.cuda.is_available()
                    else None
                )
        }

    def matte_video(
        self,
        input_video: Path,
        output_video: Path
    ):

        self.load_model()

        # RVM's official inference implementation is used
        # for temporal human matting.
        #
        # This method intentionally keeps the original
        # video timing and presenter movement.

        inference_script = Path(
            "rvm_inference.py"
        )

        if not inference_script.exists():

            raise RuntimeError(
                "RVM inference engine is not installed."
            )

        command = [

            "python",

            str(inference_script),

            "--input",
            str(input_video),

            "--output",
            str(output_video)

        ]

        subprocess.run(
            command,
            check=True
        )

        return output_video
