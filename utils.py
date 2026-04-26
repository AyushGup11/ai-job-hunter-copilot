from pypdf import PdfReader
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")

#Extract text from PDF
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text

# Analyse resume vs job description using Groq
def analyze_resume(resume_text, job_desc):

    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0
    ) 

    prompt = f"""
    You are a AI career assistant.

    Resume:
    {resume_text}

    Job Description:
    {job_desc}

    Give output in clean format:

    Match Score: (0-100)

    Missing Skills:
    - skill 1
    - skill 2

    Improvement Suggestions:
    - suggestion 1
    - suggestion 2
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content