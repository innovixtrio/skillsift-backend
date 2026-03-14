import os
from pdfminer.high_level import extract_text
import docx

# -----------------------------------
# SKILL DATABASE
# -----------------------------------

skills_db = [

# programming
"python","java","c","c++","html","css","javascript",
"react","node","django","flask",

# data science
"machine learning","data science","pandas","numpy","tensorflow",

# mobile
"flutter","android","kotlin","swift",

# ui ux
"figma","ui","ux","photoshop",

# business
"management","marketing","finance","accounting",
"sales","leadership","communication","excel","operations"
]

# -----------------------------------
# COURSES DATABASE
# -----------------------------------

ds_course = [
["Machine Learning Crash Course","https://developers.google.com/machine-learning/crash-course"],
["Machine Learning by Andrew NG","https://www.coursera.org/learn/machine-learning"],
["Data Scientist with Python","https://www.datacamp.com/tracks/data-scientist-with-python"]
]

web_course = [
["React Crash Course","https://youtu.be/Dorf8i6lCuk"],
["Node.js Course","https://youtu.be/Oe421EPjeBE"],
["Full Stack Developer","https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044"]
]

android_course = [
["Android Development Course","https://youtu.be/fis26HvvDII"],
["Flutter Course","https://youtu.be/rZLR5olMR64"]
]

uiux_course = [
["Google UX Design","https://www.coursera.org/professional-certificates/google-ux-design"],
["Adobe XD Course","https://youtu.be/68w2VwalD5w"]
]

business_course = [
["Business Analytics","https://www.coursera.org/specializations/business-analytics"],
["Marketing Fundamentals","https://www.coursera.org/learn/marketing"],
["Finance for Managers","https://www.coursera.org/learn/finance"]
]

# -----------------------------------
# VIDEOS
# -----------------------------------

resume_videos = [
"https://youtu.be/Tt08KmFfIYQ",
"https://youtu.be/y8YH0Qbu5h4",
"https://youtu.be/u75hUSShvnc"
]

interview_videos = [
"https://youtu.be/HG68Ymazo18",
"https://youtu.be/BOvAAoxM4vg"
]

# -----------------------------------
# FILE TEXT EXTRACT
# -----------------------------------

def extract_docx(path):

    doc = docx.Document(path)

    text=[]

    for p in doc.paragraphs:
        text.append(p.text)

    return "\n".join(text)


def extract_file(path):

    if path.endswith(".pdf"):
        return extract_text(path)

    elif path.endswith(".docx"):
        return extract_docx(path)

    else:
        return open(path).read()


# -----------------------------------
# SKILL DETECTION
# -----------------------------------

def detect_skills(text):

    text=text.lower()

    found=[]

    for s in skills_db:

        if s in text:
            found.append(s)

    return list(set(found))


# -----------------------------------
# FIELD PREDICTION
# -----------------------------------

def predict_field(skills):

    if "machine learning" in skills or "data science" in skills:
        return "Data Science"

    if "react" in skills or "javascript" in skills:
        return "Web Development"

    if "flutter" in skills or "android" in skills:
        return "Android Development"

    if "ui" in skills or "figma" in skills:
        return "UI UX"

    if "marketing" in skills or "finance" in skills:
        return "Business"

    return "General"


# -----------------------------------
# ANALYSIS
# -----------------------------------

def analyze_resume_file(path):

    text=extract_file(path)

    skills=detect_skills(text)

    field=predict_field(skills)

    score=min(100,len(skills)*10)

    if field=="Data Science":
        courses=ds_course

    elif field=="Web Development":
        courses=web_course

    elif field=="Android Development":
        courses=android_course

    elif field=="UI UX":
        courses=uiux_course

    elif field=="Business":
        courses=business_course

    else:
        courses=[]

    tips=[
    "Add more relevant skills",
    "Add internships",
    "Add projects",
    "Add GitHub or portfolio"
    ]

    return{
        "skills":skills,
        "score":score,
        "field":field,
        "courses":courses,
        "videos":resume_videos,
        "interview":interview_videos,
        "tips":tips
    }