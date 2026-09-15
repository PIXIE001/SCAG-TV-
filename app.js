/*
  SCAG LIVE TV
  AI NEWS STUDIO FRONTEND
*/

const API_BASE =
  window.SCAG_API_URL ||
  "http://localhost:8000";

const videoInput =
  document.getElementById("videoInput");

const mediaInput =
  document.getElementById("mediaInput");

const fileInfo =
  document.getElementById("fileInfo");

const scene =
  document.getElementById("scene");

const presenter =
  document.getElementById("presenter");

const headline =
  document.getElementById("headline");

const ticker =
  document.getElementById("ticker");

const createBtn =
  document.getElementById("createBtn");

const previewBtn =
  document.getElementById("previewBtn");

const previewVideo =
  document.getElementById("previewVideo");

const processing =
  document.getElementById("processing");

const processingTitle =
  document.getElementById("processingTitle");

const processingMessage =
  document.getElementById("processingMessage");

const progressBar =
  document.getElementById("progressBar");

const progressText =
  document.getElementById("progressText");

const sceneLabel =
  document.getElementById("sceneLabel");

const headlinePreview =
  document.getElementById("headlinePreview");

const namePreview =
  document.getElementById("namePreview");

const tickerPreview =
  document.getElementById("tickerPreview");

const resultPanel =
  document.getElementById("resultPanel");

const resultMessage =
  document.getElementById("resultMessage");

const downloadBtn =
  document.getElementById("downloadBtn");

let selectedVideo = null;
let selectedFormat = "16:9";
let currentJobId = null;


/* -------------------------
   VIDEO SELECTION
------------------------- */

videoInput.addEventListener(
  "change",
  () => {

    selectedVideo =
      videoInput.files[0] || null;

    if (!selectedVideo) {

      fileInfo.textContent =
        "No video selected";

      return;
    }

    const size =
      (
        selectedVideo.size /
        (1024 * 1024)
      ).toFixed(1);

    fileInfo.textContent =
      `${selectedVideo.name} • ${size} MB`;

    const url =
      URL.createObjectURL(
        selectedVideo
      );

    previewVideo.src = url;

    previewVideo.style.display =
      "block";
  }
);


/* -------------------------
   SUPPORTING MEDIA
------------------------- */

mediaInput.addEventListener(
  "change",
  () => {

    const count =
      mediaInput.files.length;

    if (count) {

      console.log(
        `${count} supporting media file(s) selected.`
      );
    }
  }
);


/* -------------------------
   GRAPHICS LIVE PREVIEW
------------------------- */

headline.addEventListener(
  "input",
  () => {

    headlinePreview.textContent =
      headline.value ||
      "SCAG LIVE TV NEWS";
  }
);

presenter.addEventListener(
  "input",
  () => {

    namePreview.textContent =
      presenter.value ||
      "PRESENTER";
  }
);

ticker.addEventListener(
  "input",
  () => {

    tickerPreview.textContent =
      ticker.value ||
      "DETERMINED TO EXCEL • SCAG LIVE TV";
  }
);


/* -------------------------
   FORMAT
------------------------- */

document
  .querySelectorAll(".format")
  .forEach(button => {

    button.addEventListener(
      "click",
      () => {

        document
          .querySelectorAll(".format")
          .forEach(
            item =>
              item.classList.remove(
                "active"
              )
          );

        button.classList.add(
          "active"
        );

        selectedFormat =
          button.dataset.format;

        const frame =
          document.getElementById(
            "previewFrame"
          );

        if (
          selectedFormat === "9:16"
        ) {

          frame.style.aspectRatio =
            "9 / 16";

        } else {

          frame.style.aspectRatio =
            "16 / 9";
        }
      }
    );
  });


/* -------------------------
   ORIGINAL VIDEO PREVIEW
------------------------- */

previewBtn.addEventListener(
  "click",
  () => {

    if (!selectedVideo) {

      alert(
        "Please upload a presenter video first."
      );

      return;
    }

    previewVideo.style.display =
      "block";

    previewVideo.play();
  }
);


/* -------------------------
   AI DIRECTOR
------------------------- */

createBtn.addEventListener(
  "click",
  async () => {

    if (!selectedVideo) {

      alert(
        "Please upload your presenter video first."
      );

      return;
    }

    await createProduction();
  }
);


async function createProduction() {

  resultPanel.classList.remove(
    "show"
  );

  processing.classList.add(
    "show"
  );

  setProgress(
    5,
    "Uploading video..."
  );

  const form =
    new FormData();

  form.append(
    "video",
    selectedVideo
  );

  form.append(
    "scene",
    scene.value
  );

  form.append(
    "presenters",
    "auto"
  );

  form.append(
    "headline",
    headline.value
  );

  form.append(
    "lower_third",
    presenter.value
  );

  form.append(
    "ticker",
    ticker.value
  );

  form.append(
    "format",
    selectedFormat
  );

  try {

    const response =
      await fetch(
        `${API_BASE}/api/jobs`,
        {
          method: "POST",
          body: form
        }
      );

    if (!response.ok) {

      const error =
        await response.text();

      throw new Error(error);
    }

    const data =
      await response.json();

    currentJobId =
      data.job_id;

    setProgress(
      10,
      "Video uploaded. AI Director started."
    );

    sceneLabel.textContent =
      "AI DIRECTOR PROCESSING";

    await monitorJob(
      currentJobId
    );

  } catch (error) {

    console.error(error);

    processingTitle.textContent =
      "PROCESSING ERROR";

    processingMessage.textContent =
      error.message ||
      "Unable to connect to SCAG LIVE TV server.";

    progressBar.style.width =
      "0%";

    progressText.textContent =
      "ERROR";
  }
}


/* -------------------------
   MONITOR SERVER JOB
------------------------- */

async function monitorJob(
  jobId
) {

  let finished = false;

  while (!finished) {

    const response =
      await fetch(
        `${API_BASE}/api/jobs/${jobId}`
      );

    if (!response.ok) {

      throw new Error(
        "Unable to read processing status."
      );
    }

    const job =
      await response.json();

    const progress =
      Number(job.progress || 0);

    setProgress(
      progress,
      job.message ||
      "Processing..."
    );

    if (
      job.status ===
      "complete"
    ) {

      finished = true;

      processing.classList.remove(
        "show"
      );

      sceneLabel.textContent =
        job.selected_scene ||
        "PRODUCTION COMPLETE";

      resultPanel.classList.add(
        "show"
      );

      resultMessage.textContent =
        "SCAG LIVE TV production is ready.";

      if (job.download_url) {

        downloadBtn.href =
          API_BASE +
          job.download_url;
      }

      break;
    }

    if (
      job.status ===
      "failed"
    ) {

      throw new Error(
        job.message ||
        "AI processing failed."
      );
    }

    await wait(
      1500
    );
  }
}


/* -------------------------
   PROGRESS
------------------------- */

function setProgress(
  value,
  message
) {

  const safe =
    Math.max(
      0,
      Math.min(
        100,
        Number(value)
      )
    );

  progressBar.style.width =
    `${safe}%`;

  progressText.textContent =
    `${Math.round(safe)}%`;

  processingMessage.textContent =
    message || "";
}


/* -------------------------
   UTILITY
------------------------- */

function wait(
  milliseconds
) {

  return new Promise(
    resolve =>
      setTimeout(
        resolve,
        milliseconds
      )
  );
}


/* -------------------------
   SERVER CHECK
------------------------- */

async function checkServer() {

  try {

    const response =
      await fetch(
        `${API_BASE}/health`
      );

    if (!response.ok) {
      throw new Error();
    }

    console.log(
      "SCAG LIVE TV server connected."
    );

  } catch {

    console.warn(
      "SCAG LIVE TV backend is not currently connected."
    );
  }
}

checkServer();
