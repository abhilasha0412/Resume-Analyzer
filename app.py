import streamlit as st
import PyPDF2
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="💼",
    layout="wide"
)

# -----------------------------
# ROLE SKILL DATABASE
# -----------------------------

job_roles = {

"Web Developer":[
"html","css","javascript","react","node","api","sql","bootstrap"
],

"Data Scientist":[
"python","machine learning","pandas","numpy","tensorflow","nlp"
],

"Java Developer":[
"java","spring","hibernate","jdbc","maven","rest api"
],

"HR":[
"recruitment","onboarding","payroll","talent acquisition",
"employee engagement","hr policies","training","performance management"
],

"Finance":[
"financial analysis","investment","excel","valuation",
"capital market","portfolio","equity","mutual funds"
],

"Marketing":[
"digital marketing","seo","branding","campaign",
"social media","analytics","advertising"
]

}

# -----------------------------
# COURSE SUGGESTIONS
# -----------------------------

course_links = {

"Web Developer":[
"Frontend Web Development - Coursera",
"React Developer Certification",
"JavaScript Advanced Bootcamp"
],

"Data Scientist":[
"Google Data Analytics Certification",
"Machine Learning by Andrew Ng",
"Python for Data Science"
],

"HR":[
"HR Analytics Course",
"Talent Acquisition Certification",
"Strategic HR Management"
],

"Finance":[
"Financial Markets - Yale",
"Investment Banking Certification",
"Excel for Finance"
]

}

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("📊 Resume Analyzer")

uploaded_file = st.sidebar.file_uploader(
"Upload Resume",
type=["pdf"]
)

selected_role = st.sidebar.selectbox(
"Select Target Job Role",
list(job_roles.keys())
)

experience_level = st.sidebar.selectbox(
"Experience Level",
["Fresher","1-3 Years","3-5 Years","5+ Years"]
)

jd_input = st.sidebar.text_area(
"Paste Job Description (Optional)"
)

ai_toggle = st.sidebar.toggle("AI Suggestions", True)

st.sidebar.divider()

# -----------------------------
# TITLE
# -----------------------------

st.title("💼 AI Resume Screening & Skill Analyzer")

st.write(
"Upload a resume and analyze job fit, ATS score, skill gaps and improvements."
)

# -----------------------------
# READ PDF
# -----------------------------

resume_text=""

if uploaded_file:

    reader = PyPDF2.PdfReader(uploaded_file)

    for page in reader.pages:
        resume_text+=page.extract_text()

    resume_text=resume_text.lower()

    st.success("Resume Uploaded Successfully")

# -----------------------------
# SECTION DETECTION
# -----------------------------

def detect_sections(text):

    sections={
    "Education":["education","academic"],
    "Skills":["skills","technical skills"],
    "Projects":["projects"],
    "Experience":["experience","work experience"],
    "Certifications":["certifications","certificate"]
    }

    found={}

    for sec,keywords in sections.items():

        found[sec]=any(k in text for k in keywords)

    return found

# -----------------------------
# ROLE MATCH
# -----------------------------

def role_match(text):

    scores={}

    for role,skills in job_roles.items():

        match=sum(skill in text for skill in skills)

        score=(match/len(skills))*100

        scores[role]=round(score,2)

    return dict(sorted(scores.items(),key=lambda x:x[1],reverse=True))

# -----------------------------
# RESUME SCORE
# -----------------------------

def resume_score(text):

    score=0

    if "education" in text:
        score+=20

    if "skills" in text:
        score+=20

    if "experience" in text:
        score+=20

    if "projects" in text:
        score+=20

    if "certification" in text:
        score+=10

    if len(text)>1500:
        score+=10

    return score

# -----------------------------
# SKILL GAP
# -----------------------------

def skill_gap(text,role):

    required=job_roles[role]

    missing=[skill for skill in required if skill not in text]

    return missing

# -----------------------------
# JD MATCHING
# -----------------------------

def jd_match(resume,jd):

    if jd=="":

        return 0

    jd=jd.lower()

    jd_words=set(jd.split())

    resume_words=set(resume.split())

    match=len(jd_words & resume_words)

    score=(match/len(jd_words))*100

    return round(score,2)

# -----------------------------
# MAIN ANALYSIS
# -----------------------------

if st.button("Analyze Resume"):

    if resume_text=="":

        st.warning("Upload a resume first")

    else:

        role_scores=role_match(resume_text)

        st.subheader("🎯 Role Match Score")

        for role,score in role_scores.items():

            col1,col2,col3=st.columns([3,6,1])

            with col1:
                st.write(role)

            with col2:

                if score<40:
                    st.progress(score/100)

                elif score<70:
                    st.progress(score/100)

                else:
                    st.progress(score/100)

            with col3:
                st.write(f"{score}%")

        best_role=list(role_scores.keys())[0]

        st.success(f"Best Match Role: {best_role}")

        # -----------------------------
        # RESUME SCORE
        # -----------------------------

        score=resume_score(resume_text)

        st.subheader("📊 Resume Strength Score")

        st.metric("Score",f"{score}/100")

        if score<50:
            st.error("Weak Resume")

        elif score<70:
            st.warning("Needs Improvement")

        else:
            st.success("Strong Resume")

        # -----------------------------
        # SECTION CHECK
        # -----------------------------

        st.subheader("📑 Resume Sections Check")

        sections=detect_sections(resume_text)

        for sec,val in sections.items():

            if val:
                st.success(f"{sec} Present")

            else:
                st.error(f"{sec} Missing")

        # -----------------------------
        # SKILL GAP
        # -----------------------------

        st.subheader("⚠ Missing Skills")

        missing=skill_gap(resume_text,selected_role)

        if len(missing)==0:

            st.success("No major skill gaps")

        else:

            st.write(missing)

        # -----------------------------
        # JD MATCH
        # -----------------------------

        jd_score=jd_match(resume_text,jd_input)

        if jd_input!="":

            st.subheader("📄 Job Description Match")

            st.metric("JD Match Score",f"{jd_score}%")

        # -----------------------------
        # COURSE SUGGESTIONS
        # -----------------------------

        if ai_toggle:

            st.subheader("📚 Suggested Courses")

            if selected_role in course_links:

                for course in course_links[selected_role]:

                    st.write("•",course)

        # -----------------------------
        # DOWNLOAD REPORT
        # -----------------------------

        st.subheader("📥 Download HR Report")

        if st.button("Generate Report"):

            styles=getSampleStyleSheet()

            report="resume_report.pdf"

            doc=SimpleDocTemplate(report)

            elements=[]

            elements.append(Paragraph("Resume Analysis Report",styles["Title"]))

            elements.append(Spacer(1,20))

            elements.append(Paragraph(f"Best Role Match: {best_role}",styles["Normal"]))

            elements.append(Paragraph(f"Resume Score: {score}/100",styles["Normal"]))

            elements.append(Paragraph(f"Missing Skills: {', '.join(missing)}",styles["Normal"]))

            doc.build(elements)

            with open(report,"rb") as f:

                st.download_button(
                "Download Report",
                f,
                file_name="Resume_Report.pdf"
                )