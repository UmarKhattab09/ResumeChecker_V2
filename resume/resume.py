import os 
import sys  
from dotenv import load_dotenv
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
load_dotenv()
from google import genai
import pandas as pd



API = os.getenv("GOOGLEAPI")

def geminiresponse(userinput:str):
    client = genai.Client(api_key=API)

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=userinput
    )
    return response.text



def promptgetpersoninform(pdfinput:str):

    system_prompt="""
                    You are provided a resume, extract the information in a json format. 
                    The json format must and include the person_name,email,phone, GITHUB link,PORTFOLIO link,WEBSITE link AND LINKEDIN link all of these values needs to be in a list. If the person doesn't have any of these categories. Just leave it None
                    """
    prompt = system_prompt + "\n\n"
    if pdfinput:
        prompt += f"Resume: \n{pdfinput}\n"
    prompt += "ASSISTANT:"
    output = geminiresponse(prompt)
    return output


def build_prompt(history, uploaded_text=""):
    system_prompt = """
    You are a helpful assistant. Remember user info (like name) and uploaded documents.
    """
    prompt = system_prompt + "\n\n"
    for msg in history:
        role = msg['role']
        prompt += f"{role.capitalize()}: {msg['content']}\n"
    if uploaded_text:
        prompt += f"Uploaded file:\n\"\"\"\n{uploaded_text}\n\"\"\"\n"
    prompt += "Assistant:"
    return prompt

