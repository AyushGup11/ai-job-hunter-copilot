import streamlit as st
from utils import extract_text_from_pdf, extract_skills, compare_skills, generate_suggestions, generate_resume_bullets, generate_cover_letter, extract_job_from_url, rewrite_resume

st.set_page_config(page_title="AI Job Copilot", layout="centered")

st.title("🚀 AI Job Hunter Copilot")
st.write("Analyze your resume, generate cover letters, rewrite your resume — all in one place.")

#Upload Resume
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

#Job Description
job_desc = st.text_area("Paste Job Description/Requirements")

#Job Url
job_url = st.text_input("Paste Job Link (Optional)")

# Tabs
tab1, tab2, tab3 = st.tabs([
    "📊 Resume Analysis",
    "📝 Cover Letter",
    "✨ Rewrite Resume"
])

# Tab1: Resume Analysis
with tab1:
    st.subheader("📊 Resume Analysis")
    st.write("See how well your resume matches the job, which skills you have, and what's missing.")

    if st.button("Analyze"):
        if uploaded_file and (job_desc or job_url):

            with st.spinner("Analyzing..."):

            #Extract resume text
                resume_text = extract_text_from_pdf(uploaded_file)

                if job_url:
                    job_desc = extract_job_from_url(job_url)

                    if "⚠️" in job_desc:
                        st.warning(job_desc)

                    #Extract Skills
                resume_skills = extract_skills(resume_text)
                jd_skills = extract_skills(job_desc)

                    #Compare
                matched, missing, score = compare_skills(resume_skills, jd_skills)

                    #Suggestions
                suggestions = generate_suggestions(missing)

                    #Bullet Points
                bullets = generate_resume_bullets(resume_text, job_desc)

                    # #Analyzex
                    # result = analyze_resume(resume_text, job_desc)

                    # st.subheader("📊 Analysis Result")
                    # st.write(result)

                st.success("Analysis Complete ✅")

                    #Display Results
                st.subheader(f"📊 Match Score: {score}%")

                st.subheader("📄 Extracted Job Description")
                st.write(job_desc[:1000])

                st.subheader("✅ Matched Skills")
                st.write(matched if matched else "None")

                st.subheader("❌ Missing Skills")
                st.write(missing if missing else "None")

                st.subheader("💡 Suggestions")
                st.write(suggestions)

                st.subheader("📝 Tailored Resume Bullets")
                st.write(bullets)

        else:
            st.warning("Please upload resume and add job description")


# Tab 2 : Cover Letter
with tab2:
    st.subheader("📝 Cover Letter Generator")
    st.write("Generate a personalized, professional cover letter tailored to the job.")

    if st.button("Generate Cover Letter"):
        if uploaded_file and job_desc:
            with st.spinner("Generating Cover Letter..."):
                resume_text = extract_text_from_pdf(uploaded_file)
                cover_letter = generate_cover_letter(uploaded_file, job_desc)

            st.subheader("📄 Cover Letter")
            st.write(cover_letter)

            st.download_button(
                label = "Download Cover Letter",
                data = cover_letter,
                file_name = "cover_letter.txt"
            )
        else:
            st.warning("Please upload resume and add job description")


#Tab 3: Resume
with tab3:
    st.subheader("✨ ATS-Optimized Resume Rewriter")
    st.write("Rewrite your resume to be more ATS-friendly and better aligned with the job description.")

    if st.button("✨ Rewrite Resume"):
        if uploaded_file and job_desc:
            with st.spinner("Improving your resume...."):
                new_resume = rewrite_resume(uploaded_file, job_desc)

            st.subheader("📄 Improved Resume")
            st.write(new_resume)

            st.download_button(
                label = "Download Resume",
                data = new_resume,
                file_name = "new_resume.txt"
            )
        else:
            st.warning("Please provide both resume and job description")

# improve accuracy

