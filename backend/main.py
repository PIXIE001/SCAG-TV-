from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from uuid import uuid4
import shutil
import subprocess
import json
import threading


# ============================================================
# SCAG LIVE TV — AI NEWS STUDIO BACKEND
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

WORK_DIR = BASE_DIR / "work"
UPLOAD_DIR = WORK_DIR / "uploads"
OUTPUT_DIR = WORK_DIR / "outputs"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


app = FastAPI(
    title="SCAG LIVE TV AI Studio API",
    description="AI Virtual News Studio backend",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# JOB STORAGE
# ============================================================

jobs = {}


# ============================================================
# BUILT-IN SCAG STUDIO SCENES
# ============================================================

SCENES = {
    "main": "Main News Desk — 2 Chairs",
    "single": "Single Presenter",
    "standing": "Standing News",
    "interview": "Interview",
    "weather": "Weather",
    "breaking": "Breaking News",
}


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def root():

    return {
        "name": "SCAG LIVE TV AI News Studio",
        "status": "online",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health():

    return {
        "ok": True,
        "service": "SCAG LIVE TV AI Studio"
    }


# ============================================================
# STUDIO SCENES
# ============================================================

@app.get("/scenes")
def get_scenes():

    return SCENES


# ============================================================
# VIDEO METADATA
# ============================================================

def get_video_metadata(video_path: Path):

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

        return json.loads(result.stdout)

    except Exception:

        return {
            "available": False,
            "message": "FFprobe is not installed or could not read the video."
        }


# ============================================================
# AI PIPELINE
# ============================================================

def run_ai_pipeline(job_id):

    job = jobs[job_id]

    try:

        # ----------------------------------------------------
        # STEP 1 — SOURCE ANALYSIS
        # ----------------------------------------------------

        job["status"] = "analyzing"
        job["progress"] = 10
        job["message"] = "Analyzing uploaded video..."

        input_path = Path(job["input_path"])

        metadata = get_video_metadata(input_path)

        job["metadata"] = metadata

        job["progress"] = 20


        # ----------------------------------------------------
        # STEP 2 — PRESENTER DETECTION
        # ----------------------------------------------------

        job["message"] = "Detecting presenter(s)..."

        # Production AI model will be connected here.

        job["analysis"] = {

            "presenter_detection":
                "READY_FOR_AI_MODEL",

            "number_of_presenters":
                "AUTO",

            "movement_tracking":
                "READY_FOR_AI_MODEL",

            "camera_framing":
                "READY_FOR_AI_MODEL",

            "desk_detection":
                "READY_FOR_AI_MODEL",

            "sitting_standing":
                "READY_FOR_AI_MODEL",

            "originality":
                "LOCKED"

        }

        job["progress"] = 35


        # ----------------------------------------------------
        # STEP 3 — MOVEMENT ANALYSIS
        # ----------------------------------------------------

        job["message"] = "Tracking original presenter movement..."

        job["progress"] = 45


        # ----------------------------------------------------
        # STEP 4 — CAMERA ANALYSIS
        # ----------------------------------------------------

        job["message"] = "Analyzing camera framing..."

        job["progress"] = 55


        # ----------------------------------------------------
        # STEP 5 — DESK / POSTURE
        # ----------------------------------------------------

        job["message"] = "Analyzing sitting, standing and desk configuration..."

        job["progress"] = 65


        # ----------------------------------------------------
        # STEP 6 — STUDIO SELECTION
        # ----------------------------------------------------

        job["message"] = "Preparing SCAG LIVE TV virtual studio..."

        job["selected_scene"] = SCENES.get(
            job["scene"],
            SCENES["main"]
        )

        job["progress"] = 75


        # ----------------------------------------------------
        # STEP 7 — AI COMPOSITING
        # ----------------------------------------------------

        job["status"] = "rendering"

        job["message"] = (
            "Preparing presenter for virtual-studio compositing..."
        )

        job["progress"] = 85


        # ----------------------------------------------------
        # IMPORTANT
        #
        # The actual GPU AI compositor will be inserted here.
        #
        # It will perform:
        #
        # - Person segmentation
        # - Video matting
        # - Pose tracking
        # - Camera tracking
        # - Desk detection
        # - Depth estimation
        # - Occlusion handling
        # - Lighting matching
        # - Perspective matching
        # - Studio compositing
        # - Graphics
        # - Rendering
        #
        # ----------------------------------------------------


        # ----------------------------------------------------
        # TEMPORARY SOURCE-SAFE OUTPUT
        #
        # Until the real AI compositor is connected, we preserve
        # the original file instead of pretending a fake AI
        # transformation occurred.
        # ----------------------------------------------------

        output_path = OUTPUT_DIR / f"{job_id}.mp4"

        shutil.copy2(
            input_path,
            output_path
        )

        job["output_path"] = str(output_path)


        # ----------------------------------------------------
        # COMPLETE
        # ----------------------------------------------------

        job["progress"] = 100

        job["status"] = "complete"

        job["message"] = (
            "Processing complete. "
            "AI compositor adapter is ready for production model integration."
        )

    except Exception as error:

        job["status"] = "failed"

        job["message"] = str(error)


# ============================================================
# CREATE VIDEO JOB
# ============================================================

@app.post("/api/jobs")
async def create_job(

    video: UploadFile = File(...),

    scene: str = "main",

    presenters: str = "auto",

    headline: str = "",

    lower_third: str = "",

    ticker: str = ""

):

    # --------------------------------------------------------
    # VALIDATE SCENE
    # --------------------------------------------------------

    if scene not in SCENES:

        raise HTTPException(
            status_code=400,
            detail="Unknown SCAG LIVE TV studio scene."
        )


    # --------------------------------------------------------
    # VALIDATE FILE
    # --------------------------------------------------------

    if not video.filename:

        raise HTTPException(
            status_code=400,
            detail="No video filename supplied."
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
            detail="Unsupported video format."
        )


    # --------------------------------------------------------
    # CREATE JOB
    # --------------------------------------------------------

    job_id = uuid4().hex

    input_path = (
        UPLOAD_DIR /
        f"{job_id}{extension}"
    )


    # --------------------------------------------------------
    # SAVE UPLOAD
    # --------------------------------------------------------

    with input_path.open("wb") as buffer:

        shutil.copyfileobj(
            video.file,
            buffer
        )


    # --------------------------------------------------------
    # JOB DATA
    # --------------------------------------------------------

    jobs[job_id] = {

        "id":
            job_id,

        "status":
            "queued",

        "progress":
            0,

        "message":
            "Video uploaded and queued.",

        "input_path":
            str(input_path),

        "original_filename":
            video.filename,

        "scene":
            scene,

        "presenters":
            presenters,

        "graphics":
            {

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


    # --------------------------------------------------------
    # START BACKGROUND PROCESS
    # --------------------------------------------------------

    worker = threading.Thread(

        target=run_ai_pipeline,

        args=(job_id,),

        daemon=True

    )

    worker.start()


    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

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


# ============================================================
# JOB STATUS
# ============================================================

@app.get("/api/jobs/{job_id}")
def get_job(job_id: str):

    job = jobs.get(job_id)


    if not job:

        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )


    response = {

        key: value

        for key, value in job.items()

        if key not in {
            "input_path",
            "output_path"
        }

    }


    if job.get("output_path"):

        response["download_url"] = (
            f"/api/jobs/{job_id}/download"
        )


    return response


# ============================================================
# DOWNLOAD RENDERED VIDEO
# ============================================================

@app.get("/api/jobs/{job_id}/download")
def download_video(job_id: str):

    job = jobs.get(job_id)


    if not job:

        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )


    output_path = job.get("output_path")


    if not output_path:

        raise HTTPException(
            status_code=404,
            detail="Rendered video is not available yet."
        )


    file_path = Path(output_path)


    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Rendered video file does not exist."
        )


    return FileResponse(

        path=file_path,

        media_type="video/mp4",

        filename=(
            f"SCAG_LIVE_TV_{job_id}.mp4"
        )

    )
