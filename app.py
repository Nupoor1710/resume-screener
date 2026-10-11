"""AI Resume Screening System - Streamlit UI.
Run:  streamlit run app.py
"""
import pandas as pd
import streamlit as st

from matcher import Weights, screen
from parser import read_text

st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="wide")

SAMPLE_JD = """Job Title: Machine Learning Engineer

We are looking for a Machine Learning Engineer with 3+ years of experience to build and deploy AI solutions.

Responsibilities:
- Design, train and evaluate machine learning and NLP models
- Clean and analyze data using Python, pandas and NumPy
- Build REST APIs using Flask or FastAPI to serve models
- Deploy models using Docker on AWS
- Work in an Agile team using Git

Requirements:
- Bachelor's degree in Computer Science or related field (Master's preferred)
- Strong skills in Python and SQL
- Hands-on experience with scikit-learn, TensorFlow or PyTorch
- Experience in natural language processing and deep learning
- Good problem solving and communication skills

Nice to have: Transformers, LLMs, MLOps, Kubernetes, CI/CD
"""

# ---------------- session state ----------------
if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""
if "result" not in st.session_state:
    st.session_state.result = None
if "failed" not in st.session_state:
    st.session_state.failed = []

# ---------------- header ----------------
st.title("📄 AI Resume Screening System")
st.caption("A decision-support tool for recruiters: upload a job description and resumes, "
           "get a ranked, explainable shortlist.")

# ---------------- sidebar ----------------
with st.sidebar:
    st.header("⚙️ Scoring weights")
    st.caption("Weights are normalised automatically, so they don't need to add up to 100.")
    w_skills = st.slider("Skills match", 0, 100, 50)
    w_sim = st.slider("Text similarity (TF-IDF)", 0, 100, 30)
    w_exp = st.slider("Experience", 0, 100, 10)
    w_edu = st.slider("Education", 0, 100, 10)
    st.divider()
    st.header("🔎 Display")
    top_n = st.number_input("Show top N candidates", min_value=1, max_value=500, value=10)
    min_score = st.slider("Minimum match score", 0, 100, 0)
    st.divider()
    st.caption("Tip: the skill list lives in `skills.py` - add more skills there.")

# ---------------- inputs ----------------
col_jd, col_cv = st.columns(2)

with col_jd:
    st.subheader("1️⃣ Job description")
    jd_file = st.file_uploader("Upload JD (PDF / DOCX / TXT)", type=["txt", "pdf", "docx"], key="jd_file")
    if st.button("Use sample job description"):
        st.session_state.jd_text = SAMPLE_JD
    if jd_file is not None:
        try:
            st.session_state.jd_text = read_text(jd_file.getvalue(), jd_file.name)
        except Exception as e:
            st.error(f"Could not read the JD file: {e}")
    st.text_area("Or paste / edit the job description", height=300, key="jd_text")

with col_cv:
    st.subheader("2️⃣ Resumes")
    files = st.file_uploader("Upload resumes (PDF / DOCX / TXT)", type=["pdf", "docx", "txt"],
                             accept_multiple_files=True, key="cv_files")
    if files:
        st.success(f"{len(files)} resume(s) uploaded")
    st.info("Scanned (image-only) PDFs can't be read - use text-based PDFs, DOCX or TXT.")

run = st.button("🚀 Screen candidates", type="primary")

# ---------------- run screening ----------------
if run:
    jd_text = st.session_state.jd_text
    if not jd_text.strip():
        st.warning("Please provide a job description.")
    elif not files:
        st.warning("Please upload at least one resume.")
    elif w_skills + w_sim + w_exp + w_edu == 0:
        st.warning("At least one weight must be above 0.")
    else:
        resumes, failed = [], []
        with st.spinner("Analysing resumes..."):
            for f in files:
                try:
                    text = read_text(f.getvalue(), f.name)
                    if len(text.strip()) < 30:
                        failed.append(f"{f.name} (no readable text - maybe a scanned PDF)")
                    else:
                        resumes.append((f.name, text))
                except Exception as e:
                    failed.append(f"{f.name} ({e})")
            if resumes:
                st.session_state.result = screen(jd_text, resumes,
                                                 Weights(w_skills, w_sim, w_exp, w_edu))
            else:
                st.session_state.result = None
        st.session_state.failed = failed

# ---------------- results ----------------
for msg in st.session_state.failed:
    st.warning(f"Skipped: {msg}")

df = st.session_state.result
if df is not None:
    st.divider()
    st.header("📊 Results")

    # job requirements detected
    jd_skills = df.attrs.get("jd_skills", [])
    st.subheader("Job requirements detected")
    r1, r2, r3 = st.columns([3, 1, 1])
    r1.markdown("**Skills:** " + (", ".join(jd_skills) if jd_skills else "none detected"))
    r2.metric("Min. experience", f"{df.attrs.get('jd_min_experience', 0):.0f} yrs")
    r3.metric("Education", df.attrs.get("jd_education", "-"))
    if not jd_skills:
        st.warning("No known skills were found in the job description. "
                   "Try including specific skills (e.g. Python, SQL, AWS).")

    view = df[df["Match Score"] >= min_score].head(int(top_n))
    if view.empty:
        st.info("No candidates match the current filters.")
    else:
        # summary metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Candidates screened", len(df))
        m2.metric("Top candidate", view.iloc[0]["Candidate"])
        m3.metric("Highest score", f"{view['Match Score'].max():.1f}")
        m4.metric("Average score", f"{df['Match Score'].mean():.1f}")

        # ranking table
        st.subheader("🏆 Ranking")
        st.dataframe(
            view[["Rank", "Candidate", "Match Score", "Skill Match %", "Text Similarity %",
                  "Experience (yrs)", "Education", "Email"]],
            hide_index=True,
            column_config={
                "Match Score": st.column_config.ProgressColumn("Match Score", min_value=0, max_value=100, format="%.1f"),
                "Skill Match %": st.column_config.NumberColumn(format="%.1f"),
                "Text Similarity %": st.column_config.NumberColumn(format="%.1f"),
            },
        )

        # charts
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Match score by candidate**")
            st.bar_chart(view.set_index("Candidate")["Match Score"])
        with c2:
            st.markdown("**Score components (skills vs. text similarity)**")
            st.bar_chart(view.set_index("Candidate")[["Skill Match %", "Text Similarity %"]])

        # candidate details
        st.subheader("🔍 Candidate details")
        for _, r in view.iterrows():
            label = f"#{r['Rank']}  {r['Candidate']}  -  score {r['Match Score']}"
            with st.expander(label, expanded=(r["Rank"] == 1)):
                d1, d2, d3 = st.columns(3)
                d1.metric("Skill match", f"{r['Skill Match %']:.0f}%")
                d2.metric("Experience", f"{r['Experience (yrs)']:.0f} yrs")
                d3.metric("Education", r["Education"])
                st.markdown(f"✅ **Matched skills:** {r['Matched Skills'] or '-'}")
                st.markdown(f"❌ **Missing skills:** {r['Missing Skills'] or '-'}")
                st.markdown(f"➕ **Additional skills:** {r['Other Skills'] or '-'}")
                if r["Email"]:
                    st.markdown(f"📧 {r['Email']}")
                st.caption(f"File: {r['File']}")

    # downloads
    st.subheader("⬇️ Export")
    d_a, d_b = st.columns(2)
    d_a.download_button("Download full ranking (CSV)", df.to_csv(index=False).encode("utf-8"),
                        "resume_ranking.csv", "text/csv")
    shortlist = df[df["Match Score"] >= max(min_score, 1)].head(int(top_n))
    d_b.download_button("Download shortlist (CSV)", shortlist.to_csv(index=False).encode("utf-8"),
                        "shortlist.csv", "text/csv")