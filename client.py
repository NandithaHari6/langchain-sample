import requests
import streamlit as st

def get_response(code,language):
    response=requests.post("http://localhost:8000/summary/invoke",
    json={'input':{'code':code,'language':language}})

    return response.json()['output']['content']



    ## streamlit framework

st.title('Code Summarizer')
code_input=st.text_area("Enter the code to summarize",height=20)
language=st.text_input("Enter the programming language used")

if code_input and language:
    st.write(get_response(code_input,language))

