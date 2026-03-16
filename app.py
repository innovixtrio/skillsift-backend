from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import datetime
import pandas as pd

from analyzer import analyze_resume_file
from database import connect, create_tables

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------
# DATABASE INIT
# -----------------------

create_tables()

def ensure_default_users():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR IGNORE INTO users(email,password,role)
    VALUES('admin@gmail.com','admin123','admin')
    """)

    cur.execute("""
    INSERT OR IGNORE INTO users(email,password,role)
    VALUES('user@gmail.com','user123','user')
    """)

    conn.commit()
    conn.close()

ensure_default_users()

# -----------------------
# ROOT ROUTE
# -----------------------

@app.route("/")
def home():
    return jsonify({
        "message": "SkillSift Backend Running Successfully"
    })

# -----------------------
# HEALTH CHECK
# -----------------------

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# -----------------------
# DEBUG USERS
# -----------------------

@app.route("/debug_users")
def debug_users():

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()

    conn.close()

    return jsonify(rows)

# -----------------------
# LOGIN
# -----------------------

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "ok": False,
            "message": "No JSON received"
        })

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "ok": False,
            "message": "Missing credentials"
        })

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT role FROM users WHERE email=? AND password=?",
        (email, password)
    )

    row = cur.fetchone()
    conn.close()

    if row:
        return jsonify({
            "ok": True,
            "role": row[0]
        })

    return jsonify({
        "ok": False,
        "message": "Invalid login"
    })

# -----------------------
# UPLOAD RESUME
# -----------------------

@app.route("/upload_resume", methods=["POST"])
def upload_resume():

    name = request.form.get("name")
    email = request.form.get("email")
    mobile = request.form.get("mobile")
    file = request.files.get("file")

    if not file:
        return jsonify({
            "ok": False,
            "message": "No file uploaded"
        })

    filename = file.filename
    save_path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(save_path)

    result = analyze_resume_file(save_path)

    skills = ",".join(result["skills"])
    score = result["score"]

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO resumes
    (name,email,mobile,filename,filepath,skills,score,pages,timestamp)
    VALUES(?,?,?,?,?,?,?,1,?)
    """,(
        name,
        email,
        mobile,
        filename,
        save_path,
        skills,
        score,
        str(datetime.datetime.now())
    ))

    conn.commit()
    conn.close()

    return jsonify(result)

# -----------------------
# GET RESUMES
# -----------------------

@app.route("/get_resumes")
def get_resumes():

    conn = connect()

    df = pd.read_sql_query(
        "SELECT name,email,mobile,skills,score FROM resumes",
        conn
    )

    conn.close()

    return jsonify(df.to_dict(orient="records"))

# -----------------------
# SUBMIT FEEDBACK
# -----------------------

@app.route("/submit_feedback", methods=["POST"])
def feedback():

    data = request.get_json()

    if not data:
        return jsonify({"ok": False})

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO feedback(name,email,rating,comment,timestamp)
    VALUES(?,?,?,?,datetime('now'))
    """,(
        data.get("name"),
        data.get("email"),
        data.get("rating"),
        data.get("comment")
    ))

    conn.commit()
    conn.close()

    return jsonify({"ok": True})

# -----------------------
# GET FEEDBACK STATS
# -----------------------

@app.route("/get_feedback")
def get_feedback():

    conn = connect()

    df = pd.read_sql_query(
        "SELECT rating FROM feedback",
        conn
    )

    conn.close()

    counts = df["rating"].value_counts().to_dict()

    return jsonify(counts)

# -----------------------
# ADMIN USERS
# -----------------------

@app.route("/admin/users")
def admin_users():

    conn = connect()

    df = pd.read_sql_query(
        "SELECT name,email,mobile,score FROM resumes",
        conn
    )

    conn.close()

    return jsonify({
        "users": df.to_dict(orient="records")
    })

# -----------------------
# SKILL CLUSTERS
# -----------------------

@app.route("/admin/cluster_chart")
def cluster_chart():

    conn = connect()

    df = pd.read_sql_query(
        "SELECT skills FROM resumes",
        conn
    )

    conn.close()

    clusters = {}

    for s in df["skills"].dropna():

        for skill in s.split(","):

            skill = skill.strip()

            if skill == "":
                continue

            clusters[skill] = clusters.get(skill, 0) + 1

    return jsonify(clusters)

# -----------------------
# DOWNLOAD REPORT
# -----------------------

@app.route("/download_report")
def download_report():

    conn = connect()

    df = pd.read_sql_query(
        "SELECT name,email,mobile,skills,score FROM resumes",
        conn
    )

    conn.close()

    path = os.path.join(os.path.dirname(__file__), "report.csv")

    df.to_csv(path, index=False)

    return send_file(path, as_attachment=True)

# -----------------------
# RUN SERVER
# -----------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )