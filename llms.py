from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import CrossEncoder
from langchain_groq import ChatGroq
from config import embedding_model,reranker_model,response_model
import os
from dotenv import load_dotenv
load_dotenv()

embedding_llm=HuggingFaceEmbeddings(model_name=embedding_model)
reranker_llm=CrossEncoder(reranker_model)
response_llm=ChatGroq(api_key=os.getenv("GROQ_API_KEY"),model=response_model)

