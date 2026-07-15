import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter


def get_retriever():
    pdf_path = "data/policy.pdf"
    if os.path.exists(pdf_path):
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
    else:
        print(f"Warning: {pdf_path} not found. Using placeholder policy text.")
        documents = [Document(page_content="No loan policy document found. Please provide data/policy.pdf.")]

    if not documents:
        documents = [Document(page_content="The policy document is empty. Please provide content in data/policy.pdf.")]

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings()
    db = Chroma.from_documents(texts, embeddings)
    return db.as_retriever()