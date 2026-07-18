from flask import Flask, render_template, request, url_for
import PyPDF2

app = Flask(__name__)

# ---------- Resume Text Extract ----------
def extract_text(pdf):
    text = ""
    reader = PyPDF2.PdfReader(pdf)
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


# ---------- Career Roadmap Text ----------
roadmaps = {
    "Software Developer": [
        "Programming Basics (Python / Java)",
        "DSA & Problem Solving",
        "Web Dev (HTML, CSS, JS)",
        "Frameworks (React / Django)",
        "Projects + GitHub",
        "Placement Preparation"
    ],

    "Data Scientist": [
        "Python + Statistics",
        "Pandas / NumPy",
        "Machine Learning Basics",
        "Data Visualization",
        "Projects / Kaggle",
        "Interview Prep"
    ],

    "UI/UX Designer": [
        "Design Basics",
        "Figma / Adobe XD",
        "User Research",
        "Portfolio Projects",
        "Internship Preparation"
    ]
}
company_info = {
    "Software Developer": {
        "MNC": ["Google", "Microsoft", "TCS"],
        "Startups": ["Zoho", "Freshworks"],
        "Product Companies": ["Amazon", "Flipkart","Paytm"]
    },

    "Data Scientist": {
        "MNC": ["IBM", "Accenture"],
        "Startups": ["MuSigma", "Fractal"],
        "Product": ["Meta", "Netflix"]
    },

    "UI/UX Designer": {
        "Companies": ["Adobe", "Swiggy", "Zomato"],
        "Startups": ["Design startups", "Product companies"]
    }
}


# ---------- Roadmap Images ----------
# images should be inside:
# static/images/software.png etc.
roadmap_images = {
    "Software Developer": "images/software.jpeg",
    "Data Scientist": "images/data_science.jpeg",
    "UI/UX Designer": "images/uiux.jpeg"
}

# ---- Job Role vs Required Skills ----
job_skills = {
    "Software Developer": [
        "python","java","html","css","javascript","git","dsa"
    ],
    "Data Scientist": [
        "python","statistics","pandas","numpy","machine learning"
    ],
    "UI/UX Designer": [
        "figma","adobe xd","wireframing",
        "prototyping","ui design","ux research"
    ]
}

spec_skills = {
    "Software Developer": [
        "Python", "Java", "HTML", "CSS",
        "JavaScript", "Git", "DSA", "APIs"
    ],
    "UI/UX Designer": [
        "Figma", "Wireframing", "Prototyping",
        "User Research", "Design Systems"
    ],
    "Data Scientist": [
        "Python", "Statistics", "Pandas",
        "NumPy", "Machine Learning", "SQL"
    ]
}



# ---------- Home ----------
@app.route('/')
def home():
    return render_template("index.html")


# ---------- Career Quiz ----------
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        interest = request.form['interest']

        if interest == "coding":
            result = "Software Developer"
        elif interest == "maths":
            result = "Data Scientist"
        elif interest == "design":
            result = "UI/UX Designer"
        else:
            result = "Explore Multiple Domains"

        return render_template(
            "result.html",
            result=result,
            roadmap=roadmaps.get(result, []),
            roadmap_img=roadmap_images.get(result),
            companies=company_info.get(result, {})
        )

    return render_template("quiz.html")


# ---------- Resume Analyzer ----------
@app.route('/resume', methods=['GET', 'POST'])
def resume():
    if request.method == 'POST':
        file = request.files['resume']
        role = request.form['job_role']

        text = extract_text(file).lower()

        required = job_skills.get(role, [])

        matched = [s for s in required if s in text]
        missing = [s for s in required if s not in text]

        return render_template(
            "resume_result.html",
            role=role,
            matched=matched,
            missing=missing
        )

    return render_template("resume.html")

@app.route('/spec-skill-check', methods=['POST'])
def spec_skill_check():
    role = request.form['role']
    skills = spec_skills.get(role, [])

    return render_template(
        "spec_skill.html",
        role=role,
        skills=skills
    )

@app.route('/full-report', methods=['POST'])
def full_report():
    role = request.form['role']
    matched = int(request.form['matched'])
    total = int(request.form['total'])

    resume_score = int((matched / total) * 100) if total > 0 else 0

    spec_list = spec_skills.get(role, [])

    return render_template(
        "full_report.html",
        role=role,
        resume_score=resume_score,
        spec_skills=spec_list
    )
@app.route('/final-evaluation', methods=['POST'])
def final_evaluation():
    role = request.form['role']
    resume_score = int(request.form['resume_score'])
    known = request.form.getlist('known_skills')

    total = len(spec_skills.get(role, []))
    skill_score = int((len(known) / total) * 100) if total > 0 else 0

    final_score = int((resume_score + skill_score) / 2)

    if final_score < 40:
        level = "Beginner"
    elif final_score < 70:
        level = "Intermediate"
    else:
        level = "Ready for Interview"

    missing = list(set(spec_skills.get(role, [])) - set(known))

    return render_template(
        "final_display.html",
        role=role,
        final_score=final_score,
        level=level,
        known=known,
        missing=missing
    )

if __name__ == "__main__":
    app.run(debug=True)
