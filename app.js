/*
  SCAG LIVE TV
  AI NEWS STUDIO FRONTEND
*/

/*
  IMPORTANT:
  Change this to your real backend address after deploying server.py.

  Example:
  const API_URL = "https://your-backend.example.com";
*/

const API_URL = window.SCAG_API_URL || "http://localhost:8000";


const videoInput = document.getElementById("videoInput");
const sourceVideo = document.getElementById("sourceVideo");

const scene = document.getElementById("scene");

const headline = document.getElementById("headline");
const lowerThird = document.getElementById("lowerThird");
const ticker = document.getElementById("ticker");

const directorBtn = document.getElementById("directorBtn");

const processing = document.getElementById("processing");
const processingMessage =
  document.getElementById("processingMessage");

const progressBar =
  document.getElementById("progressBar");

const progressText =
  document.getElementById("progressText");

const result =
  document.getElementById("result");

const resultVideo =
  document.getElementById("resultVideo");

const downloadBtn =
  document.getElementById("downloadBtn");

const previewStatus =
  document.getElementById("previewStatus");

const screenHeadline =
  document.getElementById("screenHeadline");


let selectedVideo = null;


/* =========================
   VIDEO SELECTION
========================= */

videoInput.addEventListener("change", () => {

  const file = videoInput.files[0];

  if (!file) {
    return;
  }

  selectedVideo = file;

  const url = URL.createObjectURL(file);

  sourceVideo.src = url;
  sourceVideo.style.display = "block";

  previewStatus.textContent = "VIDEO LOADED";

});


/* =========================
   HEADLINE PREVIEW
========================= */

headline.addEventListener("input", () => {

  const text =
    headline.value.trim() || "NEWS";

  screenHeadline.textContent = text;

});


/* =========================
   AI DIRECTOR
========================= */

directorBtn.addEventListener("click", async () => {

  if (!selectedVideo) {

    alert("Please select a presenter video first.");

    return;
  }

  processing.classList.remove("hidden");
  result.classList.add("hidden");

  directorBtn.disabled = true;

  setProgress(
    5,
    "Uploading presenter video..."
  );

  try {

    const formData = new FormData();

    formData.append(
      "video",
      selectedVideo
    );

    formData.append(
      "scene",
      scene.value
    );

    formData.append(
      "presenters",
      "auto"
    );

    formData.append(
      "headline",
      headline.value
    );

    formData.append(
      "lower_third",
      lowerThird.value
    );

    formData.append(
      "ticker",
      ticker.value
    );


    const response = await fetch(
      `${API_URL}/api/jobs`,
      {
        method: "POST",
        body: formData
      }
    );


    if (!response.ok) {

      const errorText =
        await response.text();

      throw new Error(
        errorText || "Upload failed."
      );

    }


    const job =
      await response.json();


    setProgress(
      10,
      "Video uploaded. AI Director is starting..."
    );


    await monitorJob(job.job_id);


  } catch (error) {

    console.error(error);

    processingMessage.textContent =
      "Unable to connect to the SCAG LIVE TV AI server.";

    alert(
      "AI server connection failed.\n\n" +
      "Make sure the backend is running and API_URL is correct."
    );

    directorBtn.disabled = false;

  }

});


/* =========================
   MONITOR JOB
========================= */

async function monitorJob(jobId) {

  let finished = false;


  while (!finished) {

    const response = await fetch(
      `${API_URL}/api/jobs/${jobId}`
    );


    if (!response.ok) {

      throw new Error(
        "Unable to read processing status."
      );

    }


    const job =
      await response.json();


    setProgress(
      job.progress || 0,
      job.message || "Processing..."
    );


    if (job.status === "complete") {

      finished = true;

      showResult(job);

    }


    if (job.status === "failed") {

      throw new Error(
        job.message || "Processing failed."
      );

    }


    if (!finished) {

      await sleep(1500);

    }

  }

}


/* =========================
   RESULT
========================= */

function showResult(job) {

  processing.classList.add("hidden");

  result.classList.remove("hidden");

  previewStatus.textContent =
    "PRODUCTION COMPLETE";


  if (job.download_url) {

    const url =
      API_URL + job.download_url;

    resultVideo.src = url;

    downloadBtn.href = url;

    downloadBtn.style.display =
      "inline-flex";

  } else {

    processingMessage.textContent =
      "The server completed without producing a video.";

  }


  directorBtn.disabled = false;

}


/* =========================
   PROGRESS
========================= */

function setProgress(value, message) {

  const safeValue =
    Math.max(
      0,
      Math.min(100, Number(value))
    );


  progressBar.style.width =
    `${safeValue}%`;


  progressText.textContent =
    `${Math.round(safeValue)}%`;


  processingMessage.textContent =
    message;

}


/* =========================
   HELPERS
========================= */

function sleep(ms) {

  return new Promise(
    resolve => setTimeout(resolve, ms)
  );

}
