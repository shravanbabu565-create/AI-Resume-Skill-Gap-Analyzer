from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

from analyzer import (
    extract_text_from_pdf,
    analyze_resume
)


# =========================================================
# FLASK APP CONFIGURATION
# =========================================================

app = Flask(__name__)


# Maximum upload size: 10 MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


# Upload folder
UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Create uploads folder if it doesn't exist
os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# Allowed file extensions
ALLOWED_EXTENSIONS = {
    "pdf"
}


# =========================================================
# HELPER FUNCTION
# =========================================================

def allowed_file(filename):

    if not filename:
        return False

    if "." not in filename:
        return False

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    return extension in ALLOWED_EXTENSIONS


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# ANALYZE RESUME
# =========================================================

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    try:

        # =================================================
        # GET RESUME
        # =================================================

        resume = request.files.get(
            "resume"
        )


        if not resume:

            return render_template(
                "index.html",
                error="Please upload your resume PDF."
            )


        if resume.filename == "":

            return render_template(
                "index.html",
                error="Please select a resume PDF."
            )


        if not allowed_file(
            resume.filename
        ):

            return render_template(
                "index.html",
                error="Resume must be a PDF file."
            )


        # =================================================
        # SAVE RESUME
        # =================================================

        resume_filename = secure_filename(
            resume.filename
        )


        resume_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            "resume_" + resume_filename
        )


        resume.save(
            resume_path
        )


        # =================================================
        # EXTRACT RESUME TEXT
        # =================================================

        resume_text = extract_text_from_pdf(
            resume_path
        )


        if not resume_text.strip():

            return render_template(
                "index.html",
                error=(
                    "Could not extract text from the resume. "
                    "Please make sure the PDF contains selectable text."
                )
            )


        # =================================================
        # GET JD PDF
        # =================================================

        jd_pdf = request.files.get(
            "jd_pdf"
        )


        # =================================================
        # GET JD TEXT
        # =================================================

        jd_text = request.form.get(
            "job_description",
            ""
        ).strip()


        # =================================================
        # DETERMINE JD SOURCE
        # =================================================

        job_description = ""


        # -------------------------------------------------
        # OPTION 1: JD PDF
        # -------------------------------------------------

        if (
            jd_pdf
            and jd_pdf.filename
        ):

            if not allowed_file(
                jd_pdf.filename
            ):

                return render_template(
                    "index.html",
                    error="Job Description must be a PDF file."
                )


            jd_filename = secure_filename(
                jd_pdf.filename
            )


            jd_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                "jd_" + jd_filename
            )


            jd_pdf.save(
                jd_path
            )


            # Extract JD text
            job_description = extract_text_from_pdf(
                jd_path
            )


            if not job_description.strip():

                return render_template(
                    "index.html",
                    error=(
                        "Could not extract text from the "
                        "Job Description PDF. "
                        "Please make sure the PDF contains "
                        "selectable text."
                    )
                )


        # -------------------------------------------------
        # OPTION 2: PASTED JD TEXT
        # -------------------------------------------------

        elif jd_text:

            job_description = jd_text


        # -------------------------------------------------
        # NO JD PROVIDED
        # -------------------------------------------------

        else:

            return render_template(
                "index.html",
                error=(
                    "Please upload a Job Description PDF "
                    "or paste the Job Description."
                )
            )


        # =================================================
        # ANALYZE RESUME
        # =================================================

        results = analyze_resume(
            resume_text,
            job_description
        )


        # =================================================
        # DISPLAY RESULTS
        # =================================================

        return render_template(
            "result.html",
            results=results
        )


    # =====================================================
    # FILE TOO LARGE
    # =====================================================

    except Exception as e:

        print(
            "ERROR:",
            str(e)
        )


        return render_template(
            "index.html",
            error=(
                "Something went wrong while analyzing "
                "the files. Please check your PDFs and try again."
            )
        )


# =========================================================
# HANDLE LARGE FILE ERROR
# =========================================================

@app.errorhandler(413)
def file_too_large(error):

    return render_template(
        "index.html",
        error=(
            "File too large. "
            "Please upload files smaller than 10 MB."
        )
    ), 413


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )