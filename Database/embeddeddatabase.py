from google import genai
from pypdf import PdfReader
import os 
import sys  
from dotenv import load_dotenv
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
load_dotenv()
GOOGLE=os.getenv("GOOGLEAPI")
from pinecone import Pinecone

PINECONE=os.getenv("PINECONE")
pc = Pinecone(api_key=PINECONE)
index = pc.Index("resume")




data=[]
reader =PdfReader("Resume.pdf")
page = reader.pages[0]
page_content = page.extract_text()
client = genai.Client(api_key=GOOGLE)
vectors = client.models.embed_content(
        model="gemini-embedding-001",
        contents=page_content)
embeddingvectors = vectors.embeddings
print(embeddingvectors)

data.append(
    {
        "id":"vec{}".format(1),
        "values":embeddingvectors,
        "metadata":{"text":page_content}

    }
)


index.upsert(
    vectors=data,
    namespace= "resume"
)