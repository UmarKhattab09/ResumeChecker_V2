from google import genai
from pypdf import PdfReader
import os 
import sys  
from dotenv import load_dotenv
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
load_dotenv()

from pinecone import Pinecone

# reader =PdfReader("Resume.pdf")
# page = reader.pages[0]
# page_content = page.extract_text()


class EmbeddedDatabase:
    def __init__(self,page_content):
        self.page_content=page_content
    


    

    def loadmodel(self):
        GOOGLE=os.getenv("GOOGLEAPI")
        client = genai.Client(api_key=GOOGLE)
        vectors = client.models.embed_content(
        model="gemini-embedding-001",
        contents=self.page_content)
        embedding_vector = vectors.embeddings[0].values  # ✅ Extract only the list of floats

        return embedding_vector
    
    def pushing(self):
        PINECONE=os.getenv("PINECONE")
        pc = Pinecone(api_key=PINECONE)
        index = pc.Index("resume") 
        existing_count=index.describe_index_stats()["total_vector_count"]
        print(f"EXISITING COUNT : {existing_count}, Uploading to the count : {existing_count+1}")
        vectors = self.loadmodel()
        # vectors  = vectors.embedding
        # return vectors
        data = []
        data.append(
            {
            "id":f"vec{existing_count+1}",
            "values":vectors,
            "metadata":{"text":self.page_content}
            }
        )
        index.upsert(
            vectors = data,
            namespace="resume"
        )
    

        



# test = EmbeddedDatabase(page_content=page_content)
# output = test.pushing()


