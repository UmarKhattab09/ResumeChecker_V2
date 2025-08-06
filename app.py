import streamlit as st
import random
import time
from resume.resume import geminiresponse,build_prompt,promptgetpersoninform
from Database.database import DataBase
from Database.embeddeddatabase import EmbeddedDatabase
from pypdf import PdfReader
# def geminiresponsehistory(history):
#     fullprompt = ""
#     for message in history:
#         role = message["role"]
#         content = message["content"]
#         fullprompt 

st.title("ATS RESUME CHECKER")


uploaded_file = st.file_uploader("Upload Your Resume to Enter The Database", type=["pdf"], label_visibility="collapsed")
if uploaded_file and uploaded_file.type == "application/pdf":
    # Check if file has already been processed
    if "resume_uploaded" not in st.session_state:
        reader = PdfReader(uploaded_file)
        page_content = ""
        for page in reader.pages:
            page_content += page.extract_text()

        st.session_state.page_content = page_content


        # Push to DB
        databaseloader = DataBase(page_content)
        upload = databaseloader.pushingdatabase()

        # Push to Pinecone
        pineconeloader = EmbeddedDatabase(page_content)
        uploadv2 = pineconeloader.pushing()

        # Mark as uploaded
        st.session_state.resume_uploaded = True

        st.success("Resume uploaded and embedded successfully!")
        st.write("Database response:", upload)
        st.write("Pinecone response:", uploadv2)
    else:
        st.info("Resume already uploaded in this session.")





    


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)


    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # print(prompt)
        # text = geminiresponse(prompt)
        # print(text)
        text = geminiresponse(build_prompt(st.session_state.messages, st.session_state.page_content))

        response = st.write(text)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": text})
    
