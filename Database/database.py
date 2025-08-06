#Using SUPABASE DATABASE
import os 
import sys  
from dotenv import load_dotenv
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
load_dotenv()
from resume.resume import geminiresponse
from pypdf import PdfReader
import json
from supabase import create_client, Client
url: str = os.environ.get("SUPABASEURL")
key: str = os.environ.get("SUPABASEKEY")
# reader=PdfReader("UmarKhattab_Resume.pdf")

#Most PDF are 1 page. this is for 1 page pdf for now. Will make it for multiple pages
# page = reader.pages[0] 
# page_content = page.extract_text()


class DataBase:
    def __init__(self,pdfinput:str):
        self.pdfinput = pdfinput
        
    def getpersoninform(self):

        system_prompt="""
                        You are provided a resume, extract the information in a json format. 
                        The json format must and include the person_name,email,phone, GITHUB link,PORTFOLIO link,WEBSITE link AND LINKEDIN link all of these values needs to be in a list. If the person doesn't have any of these categories. Just leave it black
                        """
        prompt = system_prompt + "\n\n"
        if self.pdfinput:
            prompt += f"Resume: \n{self.pdfinput}\n"
        prompt += "ASSISTANT:"
        return prompt

    def personinfo(self):
        output = geminiresponse(self.getpersoninform())
        cleaned_json = output.strip("```json").strip("```").strip()
        data = json.loads(cleaned_json)
        
        return data

    def pushingdatabase(self):
        data = self.personinfo()
        print(data)
        supabase: Client = create_client(url, key)
        try:
            existing = supabase.table("resume_data").select("id").eq("email", data['email'][0]).execute()
            if existing.data:
                return f"User is already on the Database"
            else:
                response = (
                supabase.table("resume_data")
                .upsert({
                    "person_name": data['person_name'][0],
                    "email": data['email'][0],
                    "phone": data['phone'][0],
                    "github_link": data.get('GITHUB link', None),
                    "portfolio_link": data.get('PORTFOLIO link',None),
                    "website_link": data.get('WEBSITE link', None),
                    "linkedin_link": data.get('LINKEDIN link',None)
                })
                .execute()
            )
                return f"Uploaded to database"
        except Exception as e:
            return f"Error PARSING the resume "
        # print(response)


# test = database(page_content)
# test.pushingdatabase()