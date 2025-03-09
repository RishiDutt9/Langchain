# Changed import to reflect current LangChain structure
from langchain_community.document_loaders import UnstructuredPDFLoader  # Fix 1: Updated import
from langchain_community.document_loaders import OnlinePDFLoader  # Note: This is unused and may still be incorrect; remove if not needed
import os
doc_path = "./Introduction to Machine Learning - Amnon Shashua - (Data Science Books).pdf"
model = "llama3.2"

# Local PDF file Upload
try:
    # Added file existence check
    if doc_path and os.path.exists(doc_path):  # Fix 2: Added os.path.exists check
        loader = UnstructuredPDFLoader(file_path=doc_path)
        data = loader.load()
        print("Data loading .....")
    else:
        print("Please provide a valid PDF file")
        exit(1)

except Exception as e:
    print(f"Error loading PDF file: {e}")

content = data[0].page_content




# =========END OF PDF injection ============

# Extract Text from PDF files and Split into Small Chunks

from langchain_community.embeddings import OllamaEmbeddings  # Updated to langchain_community
from langchain.text_splitter import RecursiveCharacterTextSplitter  # No change needed
from langchain_community.vectorstores import Chroma

# Split the Chunk
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200,chunk_overlap=300)
chunks = text_splitter.split_documents(data)
print("Done splitting......")

# print(f"Number of chunks: {len(chunks)}")
# print(f"Example chunk: {chunks[0]}")

#======= Add to vector Database =========

import ollama
from langchain_ollama import OllamaEmbeddings  # Correct import
from langchain_community.vectorstores import Chroma

ollama.pull("nomic-embed-text")

vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
    collection_name="Simpel_Rag",
)
print("Done adding to vector database......")

#=======Retrival of the most similar chunks =========
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser  # Fixed typo
from langchain_ollama import ChatOllama
from langchain.core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever  # Fixed typo

# Assuming model and vector_db are defined earlier
model = "nomic-embed-text"  # Add this if not already defined
llm = ChatOllama(model=model)

# a simple technique to generate multiple questions from a single question and then retrieve documents
# based on those questions, getting the best of both worlds.
QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI language model assistant. Your task is to generate five
    different versions of the given user question to retrieve relevant documents from
    a vector database. By generating multiple perspectives on the user question, your
    goal is to help the user overcome some of the limitations of the distance-based
    similarity search. Provide these alternative questions separated by newlines.
    Original question: {question}""",
)

retriever = MultiQueryRetriever.from_llm(
    vector_db.as_retriever(), llm, prompt=QUERY_PROMPT
)

# RAG prompt
template = """Answer the question based ONLY on the following context:
{context}
Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()  # Fixed to match import
)

res = chain.invoke(input=("WHat is Data Science",))

print(res)
