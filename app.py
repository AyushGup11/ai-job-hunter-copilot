import streamlit as st
from utils import extract_text_from_pdf, analyze_resume

st.set_page_config(page_title="AI Job Copilot", layout="wide")

st.title("🚀 AI Job Hunter Copilot")

#Upload Resume
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

#Job Description
job_desc = st.text_area("Paste Job Description/Requirements")

if st.button("Analyze"):
    if uploaded_file and job_desc:
        with st.spinner("Analyzing..."):

            #Extract resume text
            resume_text = extract_text_from_pdf(uploaded_file)

            #Analyze
            result = analyze_resume(resume_text, job_desc)

        st.subheader("📊 Analysis Result")
        st.write(result)

    else:
        st.warning("Please upload resume and add job description")

