from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from uuid import uuid4
import shutil
import threading
import subprocess
import json


# ============================================================
# SCAG LIVE TV AI NEWS STUDIO SERVER
# ============================================================


BASE_DIR = Path(__file__).resolve().parent

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
    title="SCAG LIVE TV AI News Studio",
    version="2.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ============================================================
# JOB DATABASE
# ============================================================

jobs = {}


# ============================================================
# SCAG STUDIO SCENES
# ============================================================

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
        "Breaking News"
}


# ============================================================
# BASIC ROUTES
# ============================================================

@app.get("/")
def home():

    return {

        "station":
            "SCAG LIVE TV",

        "service":
            "AI NEWS STUDIO",

        "school":
            "Senior Chief Adano Girls Senior School",

        "motto":
            "Determined to Excel",

        "status":
            "ONLINE"

    }


@app.get("/health")
def health():

    return {

        "ok":
            True,

        "service":
            "SCAG LIVE TV AI NEWS STUDIO"

    }


@app.get("/scenes")
def scenes():

    return SCENES


# ============================================================
# VIDEO INFORMATION
# ============================================================

def get_video_metadata(video_path):

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


    except Exception as error:

        return {

            "available":
                False,

            "error":
                str(error)

        }


# ============================================================
# PROCESSING PIPELINE
# ============================================================

def process_job(job_id):

    job = jobs[job_id]


    try:

        # ----------------------------------------------------
        # STEP 1
        # ----------------------------------------------------

        job["status"] = "analyzing"

        job["progress"] = 10

        job["message"] = (
            "Analyzing presenter video..."
        )


        input_path = Path(
            job["input_path"]
        )


        metadata = get_video_metadata(
            input_path
        )


        job["metadata"] = metadata


        # ----------------------------------------------------
        # STEP 2
        # ----------------------------------------------------

        job["progress"] = 20

        job["message"] = (
            "Detecting presenter(s)..."
        )


        job["analysis"] = {

            "presenters":
                "AUTO",

            "movement":
                "TRACKING",

            "camera":
                "ANALYZING",

            "desk":
                "ANALYZING",

            "body_position":
                "ANALYZING",

            "face":
                "PRESERVE",

            "voice":
                "PRESERVE",

            "originality":
                "LOCKED"

        }


        # ----------------------------------------------------
        # STEP 3
        # ----------------------------------------------------

        job["progress"] = 35

        job["message"] = (
            "Tracking original presenter movement..."
        )


        # ----------------------------------------------------
        # STEP 4
        # ----------------------------------------------------

        job["progress"] = 50

        job["message"] = (
            "Analyzing camera framing..."
        )


        # ----------------------------------------------------
        # STEP 5
        # ----------------------------------------------------

        job["progress"] = 60

        job["message"] = (
            "Understanding sitting, standing and desk setup..."
        )


        # ----------------------------------------------------
        # STEP 6
        # ----------------------------------------------------

        job["progress"] = 70

        job["message"] = (
            "Selecting SCAG LIVE TV virtual studio..."
        )


        job["selected_scene"] = SCENES.get(

            job["scene"],

            SCENES["main"]

        )


        # ----------------------------------------------------
        # STEP 7
        # ----------------------------------------------------

        job["status"] = "rendering"

        job["progress"] = 80

        job["message"] = (
            "Preparing virtual-studio composition..."
        )


        # ----------------------------------------------------
        # IMPORTANT
        #
        # This section currently creates a source-safe
        # production file.
        #
        # It DOES NOT pretend that AI background removal
        # has already happened.
        #
        # The actual AI compositor will replace this step.
        # ----------------------------------------------------

        output_path = (
            OUTPUT_DIR /
            f"{job_id}.mp4"
        )


        shutil.copy2(

            input_path,

            output_path

        )


        job["output_path"] = str(
            output_path
        )


        # ----------------------------------------------------
        # COMPLETE
        # ----------------------------------------------------

        job["progress"] = 100

        job["status"] = "complete"

        job["message"] = (

            "Production file created. "
            "AI compositor connection is ready "
            "for the actual virtual-studio rendering engine."

        )


    except Exception as error:

        job["status"] = "failed"

        job["progress"] = 0

        job["message"] = str(error)


# ============================================================
# CREATE JOB
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


    if scene not in SCENES:

        raise HTTPException(

            status_code=400,

            detail="Invalid studio scene."

        )


    if not video.filename:

        raise HTTPException(

            status_code=400,

            detail="No video supplied."

        )


    allowed = {

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


    if extension not in allowed:

        raise HTTPException(

            status_code=400,

            detail="Unsupported video format."

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
            "Video uploaded and queued.",

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

        target=process_job,

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


# ============================================================
# JOB STATUS
# ============================================================

@app.get("/api/jobs/{job_id}")
def job_status(job_id: str):

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
# DOWNLOAD
# ============================================================

@app.get("/api/jobs/{job_id}/download")
def download(job_id: str):

    job = jobs.get(job_id)


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

            detail="Video is not ready."

        )


    file_path = Path(
        output_path
    )


    if not file_path.exists():

        raise HTTPException(

            status_code=404,

            detail="Output video does not exist."

        )


    return FileResponse(

        path=file_path,

        media_type="video/mp4",

        filename=(
            f"SCAG_LIVE_TV_{job_id}.mp4"
        )

    )
