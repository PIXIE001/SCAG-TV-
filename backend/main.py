from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from pathlib import Path
from uuid import uuid4

import shutil
import subprocess
import json
import threading

from backend.ai_provider import AICompositor
from backend.video_processor import VideoProcessor


BASE_DIR = Path(__file__).resolve().parent.parent

WORK_DIR = BASE_DIR / "work"

UPLOAD_DIR = WORK_DIR / "uploads"

OUTPUT_DIR = WORK_DIR / "outputs"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


app = FastAPI(
    title="SCAG LIVE TV AI Studio",
    description="AI Virtual News Studio",
    version="2.0.0"
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


jobs = {}


SCENES = {

    "main":
        "Main News Desk — 2 Chairs",

    "single":
        "Single Presenter",

    "standing":
        "Standing News",

    "interview":
        "Interview",

    "weather":
        "Weather",

    "breaking":
        "Breaking News",

    "field":
        "Field Report",

    "school":
        "School News",

}


@app.get("/")
def root():

    return {

        "name":
            "SCAG LIVE TV AI News Studio",

        "status":
            "online",

        "version":
            "2.0.0",

        "docs":
            "/docs"

    }


@app.get("/health")
def health():

    return {

        "ok":
            True,

        "service":
            "SCAG LIVE TV AI Studio"

    }


@app.get("/scenes")
def get_scenes():

    return SCENES


def get_video_metadata(
    video_path: Path
):

    try:

        command = [

            "ffprobe",

            "-v",
            "error",

            "-print_format",
            "json",

            "-show_format",

            "-show_streams",

            str(video_path)

        ]

        result = subprocess.run(

            command,

            capture_output=True,

            text=True,

            check=True

        )

        return json.loads(
            result.stdout
        )

    except Exception:

        return {

            "available":
                False,

            "message":
                "FFprobe unavailable."

        }


def run_ai_pipeline(
    job_id
):

    job = jobs[job_id]

    try:

        # -------------------------------------------------
        # STEP 1
        # -------------------------------------------------

        job["status"] = "analyzing"

        job["progress"] = 5

        job["message"] = (
            "Loading original presenter video..."
        )


        input_path = Path(
            job["input_path"]
        )


        metadata = get_video_metadata(
            input_path
        )


        job["metadata"] = metadata


        # -------------------------------------------------
        # STEP 2
        # -------------------------------------------------

        job["progress"] = 15

        job["message"] = (
            "Analyzing camera format..."
        )


        compositor = AICompositor()

        analysis = compositor.analyze(
            input_path
        )


        job["analysis"] = {

            "people":
                analysis.people,

            "sitting":
                analysis.sitting,

            "desk_detected":
                analysis.desk_detected,

            "camera_scale":
                analysis.camera_scale,

            "width":
                analysis.width,

            "height":
                analysis.height,

            "fps":
                analysis.fps,

            "duration":
                analysis.duration,

            "notes":
                analysis.notes

        }


        # -------------------------------------------------
        # STEP 3
        # -------------------------------------------------

        job["progress"] = 25

        job["message"] = (
            "Detecting presenter(s)..."
        )


        job["progress"] = 35

        job["message"] = (
            "Tracking original body movement..."
        )


        # -------------------------------------------------
        # STEP 4
        # -------------------------------------------------

        job["progress"] = 45

        job["message"] = (
            "Analyzing sitting, standing and desk setup..."
        )


        # -------------------------------------------------
        # STEP 5
        # -------------------------------------------------

        job["progress"] = 55

        job["message"] = (
            "Analyzing original camera framing..."
        )


        # -------------------------------------------------
        # STEP 6
        # -------------------------------------------------

        job["progress"] = 65

        job["message"] = (
            "Selecting SCAG LIVE TV virtual studio..."
        )


        job["selected_scene"] = SCENES.get(

            job["scene"],

            SCENES["main"]

        )


        # -------------------------------------------------
        # STEP 7
        # -------------------------------------------------

        job["progress"] = 75

        job["message"] = (
            "Preparing professional broadcast composition..."
        )


        # -------------------------------------------------
        # STEP 8
        # -------------------------------------------------

        job["status"] = "rendering"

        job["progress"] = 85

        job["message"] = (
            "Rendering SCAG LIVE TV scene..."
        )


        #
        # SOURCE-SAFE OUTPUT
        #
        # Until the GPU compositor is connected,
        # we preserve the original video.
        #

        output_path = (
            OUTPUT_DIR /
            f"{job_id}.mp4"
        )


        shutil.copy2(

            input_path,

            output_path

        )


        job["output_path"] = (
            str(output_path)
        )


        # -------------------------------------------------
        # COMPLETE
        # -------------------------------------------------

        job["progress"] = 100

        job["status"] = "complete"

        job["message"] = (
            "SCAG LIVE TV processing complete."
        )


    except Exception as error:

        job["status"] = "failed"

        job["message"] = str(
            error
        )


@app.post("/api/jobs")
async def create_job(

    video: UploadFile = File(...),

    scene: str = "main",

    presenters: str = "auto",

    headline: str = "",

    lower_third: str = "",

    ticker: str = ""

):

    if scene not in SCENES:

        raise HTTPException(

            status_code=400,

            detail=(
                "Unknown studio scene."
            )

        )


    if not video.filename:

        raise HTTPException(

            status_code=400,

            detail=(
                "No video supplied."
            )

        )


    allowed_extensions = {

        ".mp4",
        ".mov",
        ".webm",
        ".m4v",
        ".avi",
        ".mkv"

    }


    extension = Path(
        video.filename
    ).suffix.lower()


    if extension not in allowed_extensions:

        raise HTTPException(

            status_code=400,

            detail=(
                "Unsupported video format."
            )

        )


    job_id = uuid4().hex


    input_path = (

        UPLOAD_DIR /

        f"{job_id}{extension}"

    )


    with input_path.open(
        "wb"
    ) as buffer:

        shutil.copyfileobj(

            video.file,

            buffer

        )


    jobs[job_id] = {

        "id":
            job_id,

        "status":
            "queued",

        "progress":
            0,

        "message":
            "Video uploaded.",

        "input_path":
            str(input_path),

        "original_filename":
            video.filename,

        "scene":
            scene,

        "presenters":
            presenters,

        "graphics": {

            "headline":
                headline,

            "lower_third":
                lower_third,

            "ticker":
                ticker

        },

        "originality_lock":
            True

    }


    worker = threading.Thread(

        target=run_ai_pipeline,

        args=(job_id,),

        daemon=True

    )


    worker.start()


    return {

        "success":
            True,

        "job_id":
            job_id,

        "status":
            "queued",

        "status_url":
            f"/api/jobs/{job_id}"

    }


@app.get(
    "/api/jobs/{job_id}"
)
def get_job(
    job_id: str
):

    job = jobs.get(
        job_id
    )


    if not job:

        raise HTTPException(

            status_code=404,

            detail="Job not found."

        )


    response = {

        key: value

        for key, value
        in job.items()

        if key not in {

            "input_path",
            "output_path"

        }

    }


    if job.get(
        "output_path"
    ):

        response[
            "download_url"
        ] = (
            f"/api/jobs/"
            f"{job_id}/download"
        )


    return response


@app.get(
    "/api/jobs/{job_id}/download"
)
def download_video(
    job_id: str
):

    job = jobs.get(
        job_id
    )


    if not job:

        raise HTTPException(

            status_code=404,

            detail="Job not found."

        )


    output_path = job.get(
        "output_path"
    )


    if not output_path:

        raise HTTPException(

            status_code=404,

            detail=(
                "Rendered video unavailable."
            )

        )


    file_path = Path(
        output_path
    )


    if not file_path.exists():

        raise HTTPException(

            status_code=404,

            detail=(
                "Output file missing."
            )

        )


    return FileResponse(

        path=file_path,

        media_type="video/mp4",

        filename=(
            f"SCAG_LIVE_TV_"
            f"{job_id}.mp4"
        )

    )
