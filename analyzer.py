import fitz
import re


# =========================================================
# SKILL DATABASE
# =========================================================

SKILL_CATEGORIES = {

    "Programming": [
        "python",
        "java",
        "c",
        "c++",
        "javascript",
        "typescript"
    ],

    "Web Development": [
        "html",
        "css",
        "react",
        "angular",
        "node.js",
        "flask",
        "django",
        "spring"
    ],

    "Database": [
        "sql",
        "mysql",
        "postgresql",
        "mongodb",
        "oracle"
    ],

    "Cloud & DevOps": [
        "aws",
        "azure",
        "google cloud",
        "docker",
        "kubernetes",
        "git",
        "github",
        "linux"
    ],

    "AI & Data Science": [
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "tensorflow",
        "pytorch",
        "opencv",
        "pandas",
        "numpy",
        "data science"
    ],

    "Other": [
        "rest api",
        "computer networks",
        "cybersecurity",
        "blockchain"
    ]
}


# =========================================================
# LEARNING RECOMMENDATIONS
# =========================================================

LEARNING_RESOURCES = {

    "python":
        "Learn Python fundamentals, OOP and advanced Python.",

    "java":
        "Study Java OOP, collections, exceptions and Spring basics.",

    "c":
        "Practice pointers, structures, memory management and algorithms.",

    "c++":
        "Study OOP, STL, templates and competitive programming.",

    "javascript":
        "Learn ES6+, DOM, asynchronous programming and APIs.",

    "typescript":
        "Learn TypeScript types, interfaces and generics.",

    "html":
        "Learn semantic HTML, forms and accessibility.",

    "css":
        "Learn Flexbox, Grid, responsive design and animations.",

    "react":
        "Learn components, hooks, state management and APIs.",

    "angular":
        "Learn components, services, routing and Angular CLI.",

    "node.js":
        "Learn Node.js, Express and backend API development.",

    "flask":
        "Learn Flask routing, templates, REST APIs and authentication.",

    "django":
        "Learn Django models, views, templates and REST framework.",

    "sql":
        "Practice SQL queries, joins, subqueries and database design.",

    "mysql":
        "Learn MySQL queries, indexing and database optimization.",

    "postgresql":
        "Study PostgreSQL queries, indexing and advanced SQL.",

    "mongodb":
        "Learn MongoDB documents, queries and aggregation.",

    "aws":
        "Learn EC2, S3, IAM, RDS and basic AWS architecture.",

    "azure":
        "Learn Azure VMs, storage, databases and cloud services.",

    "docker":
        "Learn Docker images, containers, Dockerfiles and Compose.",

    "kubernetes":
        "Learn pods, deployments, services and Kubernetes basics.",

    "git":
        "Practice Git branching, merging, commits and workflows.",

    "github":
        "Learn repositories, pull requests, issues and GitHub Actions.",

    "linux":
        "Practice Linux commands, shell scripting and permissions.",

    "machine learning":
        "Study supervised learning, regression, classification and evaluation.",

    "deep learning":
        "Learn neural networks, CNNs, RNNs and model training.",

    "artificial intelligence":
        "Study AI fundamentals, search, reasoning and intelligent systems.",

    "tensorflow":
        "Learn TensorFlow model creation, training and evaluation.",

    "pytorch":
        "Learn tensors, neural networks and PyTorch model training.",

    "opencv":
        "Learn image processing, object detection and computer vision.",

    "pandas":
        "Practice data cleaning, filtering, grouping and analysis.",

    "numpy":
        "Learn arrays, vectorization and numerical computing.",

    "data science":
        "Study data preprocessing, visualization and statistical analysis.",

    "rest api":
        "Learn HTTP methods, JSON, REST architecture and API authentication.",

    "computer networks":
        "Study TCP/IP, HTTP, DNS, routing and network fundamentals.",

    "cybersecurity":
        "Learn authentication, encryption, vulnerabilities and secure coding.",

    "blockchain":
        "Study blockchain architecture, hashing, consensus and smart contracts."
}


# =========================================================
# PDF TEXT EXTRACTION
# =========================================================

def extract_text_from_pdf(pdf_path):

    text = ""

    document = fitz.open(pdf_path)

    for page in document:
        text += page.get_text()

    document.close()

    return text


# =========================================================
# GET ALL SKILLS
# =========================================================

def get_all_skills():

    skills = []

    for category_skills in SKILL_CATEGORIES.values():

        skills.extend(category_skills)

    return skills


# =========================================================
# EXTRACT SKILLS
# =========================================================

def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in get_all_skills():

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):

            found_skills.append(skill)

    return sorted(set(found_skills))


# =========================================================
# CATEGORIZE SKILLS
# =========================================================

def categorize_skills(skills):

    categorized = {}

    for category, category_skills in SKILL_CATEGORIES.items():

        matched = [
            skill
            for skill in skills
            if skill in category_skills
        ]

        if matched:

            categorized[category] = matched

    return categorized


# =========================================================
# LEARNING RECOMMENDATIONS
# =========================================================

def generate_recommendations(missing_skills):

    recommendations = []

    for skill in missing_skills:

        recommendation = LEARNING_RESOURCES.get(
            skill,
            f"Develop practical knowledge of {skill}."
        )

        recommendations.append({

            "skill": skill,

            "recommendation": recommendation

        })

    return recommendations


# =========================================================
# MAIN ANALYSIS
# =========================================================

def analyze_resume(resume_text, job_description):

    # Extract skills
    resume_skills = extract_skills(
        resume_text
    )

    required_skills = extract_skills(
        job_description
    )


    # Matched skills
    matched_skills = [
        skill
        for skill in required_skills
        if skill in resume_skills
    ]


    # Missing skills
    missing_skills = [
        skill
        for skill in required_skills
        if skill not in resume_skills
    ]


    # Match percentage
    if required_skills:

        match_percentage = (
            len(matched_skills)
            /
            len(required_skills)
        ) * 100

    else:

        match_percentage = 0


    # Categorize resume skills
    resume_categories = categorize_skills(
        resume_skills
    )


    # Categorize required skills
    required_categories = categorize_skills(
        required_skills
    )


    # Generate recommendations
    recommendations = generate_recommendations(
        missing_skills
    )


    # =====================================================
    # RETURN EVERYTHING REQUIRED BY result.html
    # =====================================================

    return {

        "resume_skills":
            resume_skills,

        "required_skills":
            required_skills,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "match_percentage":
            round(
                match_percentage,
                2
            ),

        "resume_categories":
            resume_categories,

        "required_categories":
            required_categories,

        "recommendations":
            recommendations
    }