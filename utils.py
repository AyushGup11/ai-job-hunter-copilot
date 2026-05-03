from pypdf import PdfReader
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
from vector_store import create_vector_store, retrieve_context 

load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")

# 🔄 Skill normalization
SKILL_SYNONYMS = {
    "py": "python",
    "python3": "python",
    "fast api": "fastapi",
    "llms": "llm",
    "rag pipelines": "rag",
    "gen ai": "generative ai",
    "ai": "Artificial Intelligence",
    "ml": "Machine Learning",
    "apis": "API",
    "api": "API",
    "artificial Intelligence": "Artificial Intelligence"
}

def normalize_skills(skills):
    normalized = []
    for skill in skills:
        skill = skill.lower().strip()
        skill = SKILL_SYNONYMS.get(skill, skill)
        normalized.append(skill)
    return list(set(normalized))


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

    RULES:
    - Return a comma-separated list
    - No explanations
    - Normalize similar terms
    - Keep tools, frameworks, languages
    - Remove duplicates

    TEXT:
    {text}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    skills = response.content.strip()

    skills_list = [s.strip().lower() for s in skills.split(",") if s.strip()]

    return normalize_skills(skills_list)

# ⚖️ Compare skills
def compare_skills(resume_skills, jd_skills, vector_db):

    llm = ChatGroq(
        model_name = "llama-3.3-70b-versatile",
        temperature = 0.2
    )

    # Normalize 
    resume_skills = normalize_skills(resume_skills)
    jd_skills = normalize_skills(jd_skills)

    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    #basic matching
    matched = list(resume_set.intersection(jd_set))
    missing = list(jd_set.difference(resume_set))

    #  🔥 Create Vector DB (you can cache later)
    vector_db = create_vector_store()
    
    # 🔍 Query for retrieval
    query = f"""
    Resume Skills: {resume_skills}
    Job Skills: {jd_skills}
    Missing Skills: {missing}
    """
    # 🧠 REAL RAG context
    context = retrieve_context(vector_db, query)

    # 🤖 LLM reasoning with retrieved knowledge
    prompt = f"""
    You are an expert AI career assitant.

    Context:
    {context}

    Resume Skills:
    {resume_skills}

    Job Skills:
    {jd_skills}

    Missing Skills:
    {missing}

    Task:
    1. Identify most important missing skills
    2. Suggest related/alternative skills
    3. Provide a learning roadmap
    4. Highlight transferable skills

    Output in clean structured format.
    """

    insights = llm.invoke([HumanMessage(content=prompt)]).content

    #Score
    score = int((len(matched) / len(jd_skills)) * 100) if jd_skills else 0

    return matched, missing, score, insights

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

def extract_job_from_url(url):
    try:
        # ❗ Detect LinkedIn
        if "linkedin.com" in url:
            return"⚠️ LinkedIn blocks automatic extraction. Please copy-paste the job description."
        
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response =  requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        #Get all text from page
        text = soup.get_text(separator="\n")

        # Clean Text
        lines = [line.strip() for line in text.split("/n") if line.strip()]
        job_desc = "\n".join(lines[:300])  #limit size

        return job_desc
    
    except Exception as e:
        return f"Error fetching job description: {str(e)}"
    
def rewrite_resume(resume_text, job_desc):

    llm = ChatGroq(
        model_name = "llama-3.3-70b-versatile",
        temperature = 0.4 
    )

    prompt = f"""
    You are an expert resume reviewer and ATS optimization assistant.

    Task:
    Rewrite the given resume to make it more ATS-friendly and better aligned with the job description.

    Rules:
    - Improve clarity and professionalism
    - Add relevant keywords from job description
    - Keep truthfulness (do NOT invent fake experience)
    - Make bullet points strong and action-oriented
    - Optimize for AI/ATS systems

    Resume:
    {resume_text}

    job_description:
    {job_desc}

    Return:
    1. Improved Resume
    2. Key improvements made (short bullet points)
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