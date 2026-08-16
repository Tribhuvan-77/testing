from rag_workflow import vector_search
from llms import response_llm
from prompts import context_prompt
from langchain_core.prompts import ChatPromptTemplate
from rag_workflow import tree_context

query=input()

code_context=vector_search(query=query)
template=ChatPromptTemplate.from_template(context_prompt)
result_chain=template|response_llm
result=result_chain.invoke({"query":query,"code_context":code_context,"tree_context":tree_context})

print(result.content)

