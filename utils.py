from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings 
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema.document import Document
import os
import getpass
from colored import Fore, Back, Style

load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']

# Read PDF
def read_pdf(pdf_path):
    documents = []
    print(f'{Fore.white}{Back.green}"Extracting text from pdf..."{Style.reset}')
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    documents.extend(docs)
    return documents

# Split documents into chunks
def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    print(f'{Fore.white}{Back.green}"splitting documents..."{Style.reset}')
    
    # Split the documents into chunks
    chunks = text_splitter.split_documents(documents)

    return chunks

def initialize_chroma_db():
    """
    Initializes and returns a Chroma vector store with OpenAI embeddings.
    Prompts the user for the OpenAI API key if not already set in the environment.
    """
    # Check if OpenAI API key is set in the environment, if not, prompt the user to enter it
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    # Initialize Chroma vector store
    vector_store = Chroma(
        collection_name="collection",
        embedding_function=embeddings,
        persist_directory="./chroma-vdb",  # Where to save data locally, remove if not necessary
    )
    
    # Print the vector store for debugging purposes
    print(f'{Fore.white}{Back.green}"intializing vectorstore..."{Style.reset}')
    print("vectorstore:\n", vector_store)
    return vector_store

