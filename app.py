import streamlit as st
import random
import time
from resume.resume import geminiresponse,build_prompt,promptgetpersoninform
from Database.database import DataBase
from pypdf import PdfReader
# def geminiresponsehistory(history):
#     fullprompt = ""
#     for message in history:
#         role = message["role"]
#         content = message["content"]
#         fullprompt 

st.title("ATS RESUME CHECKER")


uploaded_file = st.file_uploader("Upload Your Resume to Enter The Database", type=["pdf"], label_visibility="collapsed")
if uploaded_file:


    if uploaded_file.type=="application/pdf":
        reader=PdfReader(uploaded_file)
        #Most PDF are 1 page. this is for 1 page pdf for now. Will make it for multiple pages
        page = reader.pages[0] 
        page_content = page.extract_text()
        # st.write(page.extract_text())
        databaseloader=  DataBase(page_content)
        upload = databaseloader.pushingdatabase()
        st.write(upload)




    


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
        text = geminiresponse(build_prompt(st.session_state.messages, page_content))

        response = st.write(text)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": text})
    
