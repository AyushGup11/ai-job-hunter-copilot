from pypdf import PdfReader
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")

# 📄 Extract text from PDF
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text

# 🧠 Extract skills using LLM
def extract_skills(text):
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0
    )

    prompt = f"""
    Extract ONLY technical skills from the text.

    STRICT RULES:
    - Return only skills (no explanations)
    - Remove duplicates
    - Normalize terms (e.g., "RAG pipelines" → "RAG")
    - Remove brackets, punctuation
    - Ignore degrees, soft skills, experience, roles

    Return as clean comma-separated list.

    TEXT:
    {text}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    skills = response.content.strip()

    return [s.strip().lower() for s in skills.split(",")]

# ⚖️ Compare skills
def compare_skills(resume_skills, jd_skills):
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched = list(resume_set.intersection(jd_set))
    missing = list(jd_set.difference(resume_set))

    score = int((len(matched) / len(jd_set)) * 100) if jd_set else 0

    return matched, missing, score

# 💡 Suggestions
def generate_suggestions(missing_skills):

    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.3
    )

    prompt = f"""
    The candidate is missing these skills: {missing_skills}

    Suggest:
    1. How to improve resume
    2. What to learn next

    Keep it short and practical.
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

# Generate Bullet Points
def generate_resume_bullets(resume_text, job_desc):

    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.3
    )

    prompt = f"""
    You are an expert resume writer.

    Based on the resume and job description below,
    rewrite 4-6 strong resume bullet points tailored for the job.

    Resume:
    {resume_text}

    Job Description:
    {job_desc}

    Keep bullets:
    - Impact-driven
    - Quantified if possible
    - ATS-friendly
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

def generate_cover_letter(resume_text, job_desc):

    llm = ChatGroq(
        model_name = "llama-3.3-70b-versatile",
        temperature=0.4
    ) 
    
    prompt = f"""
    You are an expert career assistant.

    Write a professional cover letter based on the resume and job description.

    Guidelines:
    - Keep it concise (200-300 words)
    - Make it personalized and job-specific
    - Highlight relevant skills and projects
    - Use a confident and professional tone
    - Avoid generic phrases

    Resume:
    {resume_text}

    Job Description:
    {job_desc}

    Format:
    - Greeting
    - 1-2 intro lines
    - Skills + experience paragraph
    - Closing paragraph
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content
 

# # Analyse resume vs job description using Groq
# def analyze_resume(resume_text, job_desc):

#     llm = ChatGroq(
#         model_name="llama-3.3-70b-versatile",
#         temperature=0
#     ) 

#     prompt = f"""
#     You are a AI career assistant.

#     Resume:
#     {resume_text}

#     Job Description:
#     {job_desc}

#     Give output in clean format:

#     Match Score: (0-100)

#     Missing Skills:
#     - skill 1
#     - skill 2

#     Improvement Suggestions:
#     - suggestion 1
#     - suggestion 2
#     """

#     response = llm.invoke([HumanMessage(content=prompt)])
#     return response.content