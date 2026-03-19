import os
import re
from pdfminer.high_level import extract_text
import docx

# -----------------------------------
# SKILL DATABASE
# -----------------------------------

skills_db = [
"python","java","c","c++","html","css","javascript",
"react","node","django","flask",
"machine learning","data science","pandas","numpy","tensorflow",
"flutter","android","kotlin","swift",
"figma","ui","ux","photoshop",
"management","marketing","finance","accounting",
"sales","leadership","communication","excel","operations"
]

# -----------------------------------
# COURSES DATABASE
# -----------------------------------

ds_course = [
["Machine Learning Crash Course","https://developers.google.com/machine-learning/crash-course"],
["Machine Learning by Andrew NG","https://www.coursera.org/learn/machine-learning"],
]

web_course = [
["React Crash Course","https://youtu.be/Dorf8i6lCuk"],
["Node.js Course","https://youtu.be/Oe421EPjeBE"],
]

android_course = [
["Flutter Course","https://youtu.be/rZLR5olMR64"]
]

uiux_course = [
["Google UX Design","https://www.coursera.org/professional-certificates/google-ux-design"]
]

business_course = [
["Business Analytics","https://www.coursera.org/specializations/business-analytics"]
]

resume_videos = [
"https://youtu.be/Tt08KmFfIYQ"
]

interview_videos = [
"https://youtu.be/HG68Ymazo18"
]

# -----------------------------------
# TEXT EXTRACTION
# -----------------------------------

def extract_docx(path):
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])


def extract_file(path):
    if path.endswith(".pdf"):
        return extract_text(path)
    elif path.endswith(".docx"):
        return extract_docx(path)
    else:
        return open(path).read()

# -----------------------------------
# 🔥 NEW: EMAIL / PHONE / NAME
# -----------------------------------

def extract_email(text):
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return emails[0] if emails else "Not found"


def extract_phone(text):
    phones = re.findall(r"\+?\d[\d\s-]{8,13}\d", text)
    return phones[0] if phones else "Not found"


def extract_name(text):
    lines = text.strip().split("\n")
    for line in lines[:5]:  # first few lines
        if len(line.split()) <= 4 and "@" not in line:
            return line.strip()
    return "User"

# -----------------------------------
# SKILL DETECTION
# -----------------------------------

def detect_skills(text):
    text = text.lower()
    return list(set([s for s in skills_db if s in text]))

# -----------------------------------
# FIELD PREDICTION
# -----------------------------------

def predict_field(skills):
    if "machine learning" in skills:
        return "Data Science"
    if "react" in skills:
        return "Web Development"
    if "flutter" in skills:
        return "Android Development"
    if "figma" in skills:
        return "UI UX"
    if "marketing" in skills:
        return "Business"
    return "General"

# -----------------------------------
# MAIN ANALYSIS
# -----------------------------------

def analyze_resume_file(path):

    text = extract_file(path)

    # 🔥 EXTRACTION
    email = extract_email(text)
    phone = extract_phone(text)
    name = extract_name(text)

    skills = detect_skills(text)
    field = predict_field(skills)
    score = min(100, len(skills) * 10)

    if field == "Data Science":
        courses = ds_course
    elif field == "Web Development":
        courses = web_course
    elif field == "Android Development":
        courses = android_course
    elif field == "UI UX":
        courses = uiux_course
    elif field == "Business":
        courses = business_course
    else:
        courses = []

    tips = [
        "Add more relevant skills",
        "Add projects",
        "Add internships",
        "Improve formatting"
    ]

    return {
        "name": name,
        "email": email,
        "contact": phone,
        "skills": skills,
        "score": score,
        "field": field,
        "courses": courses,
        "videos": resume_videos,
        "interview": interview_videos,
        "tips": tips
    }