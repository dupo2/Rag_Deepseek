import streamlit as st

from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise. Answer in detail. Dont print out <>
Question: {question} 
Context: {context} 
Answer:
"""

pdfs_directory = 'data/'
txt_directory = 'data/'

embeddings = OllamaEmbeddings(model="deepseek-r1:8b")
vector_store = InMemoryVectorStore(embeddings)

model = OllamaLLM(model="deepseek-r1:8b")

st.title(':red[PDF] RAG')
st.write('This is an app to answer questions using data from technical documents, such as user manuals.')
st.write('It is based on the principle of Retrieval-Augmented Generation (:red[RAG]) - a technique that modifies interactions with a language model so that it responds to user queries with reference to a specified set of documents.')
st.write('Upload a file below and try it out for yourself!')
st.divider()
st.write(':gray[Model currently in use:] ' + model.model)

def upload_pdf(file):
    with open(pdfs_directory + file.name, "wb") as f:
        f.write(file.getbuffer())

def upload_txt(file):
    with open(txt_directory + file.name, "wb") as f:
        f.write(file.getbuffer())

def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path)
    documents = loader.load()

    return documents

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )

    return text_splitter.split_documents(documents)

def index_docs(documents):
    vector_store.add_documents(documents)

def retrieve_docs(query):
    return vector_store.similarity_search(query)

def answer_question(question, documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    return chain.invoke({"question": question, "context": context})

def read_txt_to_array(file_path):
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines

on = st.toggle("Upload question file")
            
uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf",
    accept_multiple_files=False
)

if uploaded_file:
    upload_pdf(uploaded_file)
    documents = load_pdf(pdfs_directory + uploaded_file.name)
    chunked_documents = split_text(documents)
    index_docs(chunked_documents)
    st.chat_message("user").write(f"Finished indexing {uploaded_file.name}")
    st.chat_message("assistant").write("Ready to answer questions")

    question = st.chat_input()

    if question:
        st.chat_message("user").write(question)
        related_documents = retrieve_docs(question)
        answer = answer_question(question, related_documents)
        answer
        st.chat_message("assistant").write(answer)

if on:
    question_file = st.file_uploader(
    "Upload questions TXT",
    type="txt",
    accept_multiple_files=False
)
    if question_file: 
        upload_txt(question_file)
        lines_array = read_txt_to_array(txt_directory + question_file.name)
        for question in lines_array:
            print(question)
            st.chat_message("user").write(f"Asking question: {question}")
            related_documents = retrieve_docs(question)
            answer = answer_question(question, related_documents)
            st.chat_message("assistant").write(answer)
          
