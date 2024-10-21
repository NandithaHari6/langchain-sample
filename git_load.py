# Clone
from git import Repo
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain_text_splitters import CharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain, StuffDocumentsChain
from dotenv import load_dotenv
from langchain.chains.summarize import load_summarize_chain
load_dotenv()
import os

repo_path = "Users\\Hari\\OneDrive\\Desktop\\Ammu\\Langchain Codebasics\\langchain-sample\\price-comp"
# repo = Repo.clone_from("https://github.com/NandithaHari6/Price-comparison-website", to_path=repo_path)
loader = GenericLoader.from_filesystem(
    repo_path ,
    glob="**/*",
    suffixes=[".py"],
    exclude=["**/non-utf8-encoding.py"],
    parser=LanguageParser(language=Language.PYTHON),
)
documents = loader.load()
print("Len of documents")
print(len(documents))
# for i in range(len(documents)):

#     print(i, documents[i].page_content)
#     print("\n\n")
from langchain_text_splitters import RecursiveCharacterTextSplitter

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON, chunk_size=2000, chunk_overlap=200
)
texts = python_splitter.split_documents(documents)
len(texts)


llm=ChatGroq(temperature=0,
             groq_api_key=os.getenv("groq_api_key"),
             model_name="llama-3.1-70b-versatile")

# Map
map_template = """The following is a set of docs
{docs}
The docs contain python code for building a proce comparison website. Please summarize each doc in 2 to 3 lines, include all necessary and important information."""
map_prompt = PromptTemplate.from_template(map_template)
map_chain = map_prompt |llm

# Reduce
reduce_template = """The following is set of summaries:
{docs}
Take these and distill it into a final, consolidated summary of the main themes. 
"""
reduce_prompt = PromptTemplate.from_template(reduce_template)
# Run chain
reduce_chain = reduce_prompt |llm

# Takes a list of documents, combines them into a single string, and passes this to an LLMChain
combine_documents_chain= create_stuff_documents_chain(llm, reduce_prompt,document_variable_name="docs")
# Combines and iteratively reduces the mapped documents
# reduce_documents_chain = ReduceDocumentsChain(
#     # This is final chain that is called.
#     combine_documents_chain=combine_documents_chain,
#     # If documents exceed context for `StuffDocumentsChain`
#     collapse_documents_chain=combine_documents_chain,
#     # The maximum number of tokens to group documents into.
#     token_max=4000,
# )
res=reduce_chain.invoke({'docs':texts})
print(res)