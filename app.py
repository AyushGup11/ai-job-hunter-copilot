import streamlit as st
from utils import extract_text_from_pdf, extract_skills, compare_skills, generate_suggestions, generate_resume_bullets, generate_cover_letter, extract_job_from_url, rewrite_resume
from vector_store import create_vector_store, retrieve_context
import matplotlib.pyplot as plt
import numpy as np
@st.cache_resource
def load_vector_db():
    return create_vector_store()

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

                # 🌐 Extract job from URL if provided
                final_job_desc = job_desc
                if job_url:
                    extracted = extract_job_from_url(job_url)

                    if "⚠️" in extracted:
                        st.warning(extracted)
                    else:
                        final_job_desc = extracted

                    #Extract Skills
                resume_skills = extract_skills(resume_text)
                jd_skills = extract_skills(final_job_desc[:3000])

                # 🔥 Load vector DB (cached)
                vector_db = load_vector_db()

                    #Compare
                matched, missing, score, insights = compare_skills(
                    resume_skills,
                    jd_skills, 
                    vector_db
                )

                    #Suggestions
                suggestions = generate_suggestions(missing)

                    #Bullet Points
                bullets = generate_resume_bullets(resume_text, final_job_desc)

                    # #Analyzex
                    # result = analyze_resume(resume_text, job_desc)

                    # st.subheader("📊 Analysis Result")
                    # st.write(result)

                st.success("Analysis Complete ✅")

                # 📊 Score
                st.markdown("### 📊 Match Score")
                st.progress(score / 100)
                st.metric(label="Match %", value=f"{score}%")

                # 📄 Job Description Preview
                st.markdown("### 📄 Job Description")
                st.write(final_job_desc[:800])

                #Tabs inside tab (🔥 UI upgrade)
                subtab1, subtab2, subtab3 = st.tabs(["✅ Skills", "🧠 Insights", "💡 Suggestions"])

                with subtab1:
                    st.markdown("### ✅ Matched Skills")
                    st.write(matched if matched else "None")

                    st.markdown("### ❌ Missing Skills")
                    for skill in missing:
                        st.write(f"- {skill}")

                    # 📊 Skill Gap Visualization
                    st.markdown("### 📊 Skill Gap Visualization")

                    all_skills = sorted(list(set(resume_skills + jd_skills)))[:20]
                    values = [1 if skill in resume_skills else 0 for skill in all_skills]

                    fig, ax = plt.subplots()

                    labels = [skill[:15] + "..." if len(skill) > 15 else skill for skill in all_skills]

                    ax.barh(labels, values)

                    ax.set_xlabel("Presence (1 = Have, 0 = Missing)")
                    ax.set_title("Skill Gap")

                    plt.tight_layout()
                    st.pyplot(fig)
                    
                with subtab2:
                    st.markdown("### 🧠 AI Insights")
                    st.write(insights)

                with subtab3:
                    st.markdown("### 📝 Tailored Resume Bullets")
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
                cover_letter = generate_cover_letter(resume_text, job_desc)

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
                resume_text = extract_text_from_pdf(uploaded_file)
                new_resume = rewrite_resume(resume_text, job_desc) 

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

