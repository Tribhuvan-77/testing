# # from pathlib import Path

# # cwd=Path.cwd()

# # print(cwd)


# with open("/Users/tulluritribhuvan/learning/langgraph/agents/code/code_fixer.py","r",encoding="utf-8") as file:
#     content=file.read()
#     print(content)


from llms import embedding_llm,reranker_llm
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from config import chunksize

from sum_generator import file_sum_generator,chunk_sum_generator
from Directory import Directory_Tree
from pathlib import Path
import shutil
import ast

root="/Users/tulluritribhuvan/learning/langgraph"

root=Path(root)

tree_context=Directory_Tree(root)

loader=DirectoryLoader(path=str(root),glob="**/*.py")
vector_store=Chroma(collection_name=root.name,embedding_function=embedding_llm,persist_directory="./chroma_langchain_db")

result=loader.load()

for i in result:
        functions=[]
        variables=[]
        classes=[]
        file_sum=file_sum_generator(i.page_content)
        with open(i.metadata["source"],"r") as file:
            code=file.read()
        tree=ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node,ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node,ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node,ast.Assign):
                for target in node.targets:
                 if isinstance(target, ast.Name):
                    variables.append(target.id)  
        if functions:  
         i.metadata["functions"]=functions
        if classes:
         i.metadata["classes"]=classes
        if variables:
         i.metadata["variables"]=variables
        if file_sum:
         i.metadata["file_sum"]=file_sum

textsplitter=RecursiveCharacterTextSplitter(chunk_size=chunksize)
chunks=textsplitter.split_documents(result)

for i in chunks:
    chunk_sum=chunk_sum_generator(i.metadata.get("file_sum"),i.page_content)
    i.metadata["chunk_sum"]=chunk_sum
    context=""
    context+=f"""
"Chunk_summary: {chunk_sum}
File: {i.metadata.get("source")}
Functions: {i.metadata.get("functions")}
Classes: {i.metadata.get("classes")}
"""
    i.page_content=context+i.page_content

if vector_store._collection.count()>0:
   print("Collection already exists")
else:
 vector_store.add_documents(chunks)
 
retriever=vector_store.as_retriever(search_type="similarity",search_kwargs={"k":5})


def vector_search(query:str):
    result=retriever.invoke(query)
    # for i,j in enumerate(result):
    #     print(f"{i}. metadata={j.metadata} page_content={j.page_content}")
    return result
    

