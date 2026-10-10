import os
from click import prompt
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def analyze_resume(resume_text):

    prompt = f"""
You are an expert resume reviewer.

Analyze the following resume.

Return:

1. Resume Score (0-100)
2. ATS Score (0-100)
3. Strengths
4. Weaknesses
5. Missing Skills
6. Suggestions

Resume:

{resume_text}
"""
    
    

    response = client.responses.create(
    model="gemini-2.0-flash",
    contents=prompt
)

    return response.text