import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
import os

# --- Document Processing ---

def get_document_text(uploaded_files):
    """
    Extracts text from a list of uploaded files (PDF, DOCX, TXT).
    
    Args:
        uploaded_files: A list of files uploaded via Streamlit's file_uploader.

    Returns:
        A single string containing the concatenated text from all documents.
    """
    text = ""
    for uploaded_file in uploaded_files:
        try:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            if file_extension == ".pdf":
                pdf_reader = PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            elif file_extension == ".docx":
                doc = Document(uploaded_file)
                for para in doc.paragraphs:
                    text += para.text + "\n"
            elif file_extension == ".txt":
                text += uploaded_file.getvalue().decode("utf-8")
        except Exception as e:
            st.error(f"Error processing file {uploaded_file.name}: {e}")
    return text

def get_text_chunks(text):
    """
    Splits a long string of text into smaller chunks for processing.
    
    Args:
        text: The input string.

    Returns:
        A list of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# --- AI/ML and Vector Store ---

@st.cache_resource
def get_vectorstore(text_chunks):
    """
    Creates a FAISS vector store from text chunks using HuggingFace embeddings.
    Caches the result to avoid re-computation on every run.

    Args:
        text_chunks: A list of text chunks.

    Returns:
        A FAISS vector store object.
    """
    # Using a high-quality, open-source embedding model that runs locally
    # Note: The first time this runs, it will download the model (~1.3 GB)
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    """
    Creates a conversational retrieval chain.

    Args:
        vectorstore: A FAISS vector store object.

    Returns:
        A ConversationalRetrievalChain object.
    """
    llm = ChatOpenAI(temperature=0.2) # Lower temperature for more factual responses
    
    # Memory to store chat history and provide context for follow-up questions
    memory = ConversationBufferMemory(
        memory_key='chat_history', 
        return_messages=True
    )
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain