/* =========================================
   ELEMENTS
========================================= */

const resumeInput =
    document.getElementById("resume");

const resumeUploadBox =
    document.getElementById("resumeUploadBox");

const resumeSelectedFile =
    document.getElementById("resumeSelectedFile");

const resumeFileName =
    document.getElementById("resumeFileName");

const removeResume =
    document.getElementById("removeResume");


const jdInput =
    document.getElementById("jd_pdf");

const jdUploadBox =
    document.getElementById("jdUploadBox");

const jdSelectedFile =
    document.getElementById("jdSelectedFile");

const jdFileName =
    document.getElementById("jdFileName");

const removeJD =
    document.getElementById("removeJD");


const pdfTab =
    document.getElementById("pdfTab");

const textTab =
    document.getElementById("textTab");

const jdPdfSection =
    document.getElementById("jdPdfSection");

const jdTextSection =
    document.getElementById("jdTextSection");


const jobDescription =
    document.getElementById("jobDescription");

const charCount =
    document.getElementById("charCount");


const analyzerForm =
    document.getElementById("analyzerForm");

const analyzeButton =
    document.getElementById("analyzeButton");


/* =========================================
   JD MODE
========================================= */

let jdMode = "pdf";


pdfTab.addEventListener(
    "click",
    function () {

        jdMode = "pdf";

        pdfTab.classList.add("active");

        textTab.classList.remove("active");

        jdPdfSection.classList.remove("hidden");

        jdTextSection.classList.add("hidden");

        jobDescription.removeAttribute("required");

    }
);


textTab.addEventListener(
    "click",
    function () {

        jdMode = "text";

        textTab.classList.add("active");

        pdfTab.classList.remove("active");

        jdTextSection.classList.remove("hidden");

        jdPdfSection.classList.add("hidden");

        jobDescription.setAttribute(
            "required",
            "required"
        );

    }
);


/* =========================================
   RESUME UPLOAD
========================================= */

resumeInput.addEventListener(
    "change",
    function () {

        if (this.files.length > 0) {

            showResume(
                this.files[0]
            );

        }

    }
);


function showResume(file) {

    resumeFileName.textContent =
        file.name;

    resumeSelectedFile.classList.add(
        "show"
    );

    document.getElementById(
        "resumeUploadTitle"
    ).textContent =
        "Resume selected ✓";

}


/* =========================================
   REMOVE RESUME
========================================= */

removeResume.addEventListener(
    "click",
    function (event) {

        event.preventDefault();

        event.stopPropagation();

        resumeInput.value = "";

        resumeSelectedFile.classList.remove(
            "show"
        );

        document.getElementById(
            "resumeUploadTitle"
        ).textContent =
            "Drop your resume here";

    }
);


/* =========================================
   JD PDF
========================================= */

jdInput.addEventListener(
    "change",
    function () {

        if (this.files.length > 0) {

            showJD(
                this.files[0]
            );

        }

    }
);


function showJD(file) {

    jdFileName.textContent =
        file.name;

    jdSelectedFile.classList.add(
        "show"
    );

    document.getElementById(
        "jdUploadTitle"
    ).textContent =
        "Job Description selected ✓";

}


/* =========================================
   REMOVE JD
========================================= */

removeJD.addEventListener(
    "click",
    function (event) {

        event.preventDefault();

        event.stopPropagation();

        jdInput.value = "";

        jdSelectedFile.classList.remove(
            "show"
        );

        document.getElementById(
            "jdUploadTitle"
        ).textContent =
            "Upload Job Description PDF";

    }
);


/* =========================================
   RESUME DRAG & DROP
========================================= */

resumeUploadBox.addEventListener(
    "dragover",
    function (event) {

        event.preventDefault();

        resumeUploadBox.classList.add(
            "dragover"
        );

    }
);


resumeUploadBox.addEventListener(
    "dragleave",
    function () {

        resumeUploadBox.classList.remove(
            "dragover"
        );

    }
);


resumeUploadBox.addEventListener(
    "drop",
    function (event) {

        event.preventDefault();

        resumeUploadBox.classList.remove(
            "dragover"
        );

        const files =
            event.dataTransfer.files;

        if (files.length > 0) {

            resumeInput.files =
                files;

            showResume(
                files[0]
            );

        }

    }
);


/* =========================================
   JD DRAG & DROP
========================================= */

jdUploadBox.addEventListener(
    "dragover",
    function (event) {

        event.preventDefault();

        jdUploadBox.classList.add(
            "dragover"
        );

    }
);


jdUploadBox.addEventListener(
    "dragleave",
    function () {

        jdUploadBox.classList.remove(
            "dragover"
        );

    }
);


jdUploadBox.addEventListener(
    "drop",
    function (event) {

        event.preventDefault();

        jdUploadBox.classList.remove(
            "dragover"
        );

        const files =
            event.dataTransfer.files;

        if (files.length > 0) {

            jdInput.files =
                files;

            showJD(
                files[0]
            );

        }

    }
);


/* =========================================
   CHARACTER COUNT
========================================= */

jobDescription.addEventListener(
    "input",
    function () {

        charCount.textContent =
            this.value.length;

    }
);


/* =========================================
   FORM VALIDATION
========================================= */

analyzerForm.addEventListener(
    "submit",
    function (event) {

        /*
         * Resume is always required.
         */

        if (!resumeInput.files.length) {

            event.preventDefault();

            alert(
                "Please upload your resume PDF."
            );

            return;

        }


        /*
         * If PDF mode is selected,
         * JD PDF must be provided.
         */

        if (
            jdMode === "pdf" &&
            !jdInput.files.length
        ) {

            event.preventDefault();

            alert(
                "Please upload the Job Description PDF."
            );

            return;

        }


        /*
         * If text mode is selected,
         * JD text must be provided.
         */

        if (
            jdMode === "text" &&
            !jobDescription.value.trim()
        ) {

            event.preventDefault();

            alert(
                "Please paste the Job Description."
            );

            return;

        }


        /*
         * Loading animation
         */

        analyzeButton.disabled = true;

        analyzeButton.innerHTML = `

            <span>
                ⟳
            </span>

            <span>
                Analyzing...
            </span>

        `;

    }
);