import streamlit as st
import pickle
import numpy as np
import PyPDF2

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Sidebar: Welcome + Theme
# -----------------------------
with st.sidebar:
    st.markdown("## 👋 Welcome!")
    user_name = st.text_input("Enter your name", "Candidate")
    theme = st.radio("Choose Theme", ["Light 🌞", "Dark 🌙"])

# -----------------------------
# Apply theme via CSS
# -----------------------------
if theme == "Dark 🌙":
    primary_bg = "#0E1117"
    text_color = "#FAFAFA"
    card_bg = "#1F2937"
    badge_missing = "#EF4444"
    badge_present = "#10B981"
else:  # Light Theme
    primary_bg = "#FAFAFA"
    text_color = "#0E1117"
    card_bg = "#E5E7EB"
    badge_missing = "#EF4444"
    badge_present = "#10B981"

st.markdown(
    f"""
    <style>
    .main {{
        background-color: {primary_bg};
        color: {text_color};
    }}
    .stButton>button {{
        background-color: {card_bg};
        color: {text_color};
    }}
    .card {{
        background-color: {card_bg};
        border-radius:10px;
        padding:15px;
        margin:10px 0;
        color: {text_color};
    }}
    .badge {{
        display:inline-block;
        padding:3px 10px;
        border-radius:5px;
        margin:2px;
        background-color:{badge_missing};
        color:white;
        font-weight:bold;
    }}
    .badge.present {{
        background-color:{badge_present};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(f"### Welcome, {user_name}! Let's analyze your resume 💼")

# -----------------------------
# Load Model & Vectorizer
# -----------------------------
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# -----------------------------
# Important Skills Dictionary
# -----------------------------
job_skills = {
    "Web Application Developer": [
        "html", "css", "javascript", "react", "node", "django",
        "flask", "api", "sql", "bootstrap"
    ],
    "Data Scientist": [
        "python", "machine learning", "tensorflow",
        "pandas", "numpy", "data analysis", "nlp"
    ],
    "Java Developer": [
        "java", "spring", "hibernate", "jdbc",
        "sql", "maven", "rest api"
    ],
    "HR": [  # New HR/MBA role
        "recruitment", "onboarding", "payroll", "employee engagement",
        "talent acquisition", "training", "performance evaluation", "hr policies"
    ]
}

# -----------------------------
# Title Banner
# -----------------------------
st.markdown(
    f"""
    <div style="text-align:center; padding:15px; background-color:#4F46E5; color:white; border-radius:10px;">
        <h1>💼 AI Resume Screening & Skill Analyzer</h1>
        <p>Upload your resume and discover your top job fit with skill gaps 🚀</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Upload Resume
# -----------------------------
uploaded_file = st.file_uploader("📂 Upload Resume (PDF only)", type=["pdf"])
resume_text = ""

if uploaded_file is not None:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        resume_text += page.extract_text()
    st.success("✅ Resume uploaded successfully!")

# -----------------------------
# Analyze Resume
# -----------------------------
if st.button("🔍 Analyze Resume"):
    if resume_text.strip() == "":
        st.warning("⚠️ Please upload a resume first.")
    else:
        transformed_text = vectorizer.transform([resume_text])
        probabilities = model.predict_proba(transformed_text)[0]
        classes = model.classes_
        results = sorted(zip(classes, probabilities), key=lambda x: x[1], reverse=True)

        # -----------------------------
        # Dashboard Cards for Top 3 Roles
        # -----------------------------
        st.subheader("🎯 Top Predicted Roles")
        for role, prob in results[:3]:
            percentage = round(prob * 100, 2)
            st.markdown(
                f"""
                <div class="card">
                    <h4>{role} — {percentage}%</h4>
                    <progress value="{prob}" max="1" style="width:100%; height:15px;"></progress>
                </div>
                """,
                unsafe_allow_html=True
            )

        best_role = results[0][0]
        best_score = round(results[0][1] * 100, 2)
        st.success(f"🏆 Best Match: {best_role} ({best_score}%)")

        # -----------------------------
        # Skill Gap Analysis with Badges
        # -----------------------------
        st.subheader("📌 Skill Gap Analysis")
        resume_lower = resume_text.lower()
        required_skills = job_skills.get(best_role, [])

        skill_badges = ""
        for skill in required_skills:
            if skill in resume_lower:
                skill_badges += f'<span class="badge present">{skill}</span>'
            else:
                skill_badges += f'<span class="badge">{skill}</span>'

        st.markdown(skill_badges, unsafe_allow_html=True)

        # -----------------------------
        # HR Specific Tip
        # -----------------------------
        if best_role == "HR":
            st.info(
                "💡 Tip: Highlight HR certifications, employee engagement projects, and payroll experience "
                "to improve your chances in recruitment roles."
            )

        # Suggest improvement if score < 80%
        if best_score < 80:
            st.error(
                "🚀 To increase your selection chance above 80%, consider adding more relevant skills "
                "and project experience related to this role."
            )