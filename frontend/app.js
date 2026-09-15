const API_URL =
    "YOUR_BACKEND_URL";


const videoInput =
    document.getElementById(
        "videoInput"
    );


const createButton =
    document.getElementById(
        "createAI"
    );


const statusBox =
    document.getElementById(
        "status"
    );


const progressBar =
    document.getElementById(
        "progress"
    );


const resultVideo =
    document.getElementById(
        "resultVideo"
    );


let currentJob = null;


function setStatus(
    message
) {

    if (statusBox) {

        statusBox.textContent =
            message;

    }

}


function setProgress(
    value
) {

    if (progressBar) {

        progressBar.value =
            value;

    }

}


async function createAIStudio() {

    if (!videoInput) {

        alert(
            "Video upload control not found."
        );

        return;

    }


    const file =
        videoInput.files[0];


    if (!file) {

        alert(
            "Please upload a presenter video first."
        );

        return;

    }


    const form =
        new FormData();


    form.append(
        "video",
        file
    );


    form.append(
        "scene",
        "main"
    );


    form.append(
        "presenters",
        "auto"
    );


    form.append(
        "headline",
        ""
    );


    form.append(
        "lower_third",
        ""
    );


    form.append(
        "ticker",
        ""
    );


    setStatus(
        "Uploading video..."
    );


    setProgress(5);


    try {

        const response =
            await fetch(
                `${API_URL}/api/jobs`,
                {
                    method:
                        "POST",

                    body:
                        form
                }
            );


        if (!response.ok) {

            throw new Error(
                await response.text()
            );

        }


        const data =
            await response.json();


        currentJob =
            data.job_id;


        monitorJob(
            currentJob
        );


    } catch (error) {

        setStatus(
            "Upload failed: " +
            error.message
        );

    }

}


async function monitorJob(
    jobId
) {

    try {

        const response =
            await fetch(
                `${API_URL}/api/jobs/${jobId}`
            );


        const job =
            await response.json();


        setProgress(
            job.progress || 0
        );


        setStatus(
            job.message || "Processing..."
        );


        if (
            job.status ===
            "complete"
        ) {

            setStatus(
                "SCAG LIVE TV studio ready."
            );


            if (
                resultVideo &&
                job.download_url
            ) {

                resultVideo.src =
                    API_URL +
                    job.download_url;

                resultVideo.controls =
                    true;

            }


            return;

        }


        if (
            job.status ===
            "failed"
        ) {

            setStatus(
                "Processing failed: " +
                job.message
            );

            return;

        }


        setTimeout(
            () =>
                monitorJob(
                    jobId
                ),
            2000
        );


    } catch (error) {

        setStatus(
            "Connection error: " +
            error.message
        );

    }

}


if (createButton) {

    createButton.addEventListener(
        "click",
        createAIStudio
    );

}
