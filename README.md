## This is update of my old ResumeAtsChecker. 


### Some updates i've done
- One of them is connecting SupaBase for extracting the information from the pdf and saving it on supabase instead of local
- Using Pinecone and embedding the resume for RAG Purpose
- Moreover, resume will be uploaded to supabase when uploaded, and it will answer the questions relating to the resume. However one problem is that I am working on fixing a bug so instead of trying to upload the resume again and again whenever asked a question. It's gonna do it only one time







- So Previous updates from the old one, add basically history session and using pypdf to extract the pdf.

- Thinking of putting into a  bunch of pdfs on a database and create a prompt that that fetches all of the resumes related to that particular job description. 

- Let's see how far I can take this