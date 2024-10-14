groq_api_key="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"
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langserve import add_routes
from fastapi import FastAPI
import uvicorn
import os
llm=ChatGroq(temperature=0,
             groq_api_key=groq_api_key,
             model_name="llama-3.1-70b-versatile")


app=FastAPI(
    title="Langchain Server",
    version="1.0",
    decsription="A simple API Server"

)

prompt_extract = PromptTemplate.from_template(
        """
        ### This is the code in {language} programming  language:
        {code}
        ### INSTRUCTION:
        Summarize the code in no more than 400 words. Clearly explain the functionality of the code
        ### NO PREAMBLE:    
        """
)




add_routes(
    app,
    prompt_extract|llm,
    path="/summary"


)


if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)