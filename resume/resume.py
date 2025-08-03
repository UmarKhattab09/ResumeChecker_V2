import os 
import sys  
from dotenv import load_dotenv
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
load_dotenv()
from google import genai



API = os.getenv("GOOGLEAPI")

def geminiresponse(userinput:str):
    client = genai.Client(api_key=API)

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=userinput
    )
    return response.text



    