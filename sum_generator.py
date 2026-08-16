from llms import response_llm
from langchain_core.prompts import ChatPromptTemplate
from prompts import chunk_summary_prompt,file_summary_prompt


def file_sum_generator(file_code:str):
    file_template=ChatPromptTemplate.from_template(file_summary_prompt)
    chain=file_template|response_llm

    result=chain.invoke({"code":file_code})
    return result.content

def chunk_sum_generator(file_sum:str,chunk_code:str):
    chunk_template=ChatPromptTemplate.from_template(chunk_summary_prompt)
    chain=chunk_template|response_llm

    result=chain.invoke({"file_summary":file_sum,"chunk":chunk_code})
    return result.content

