import os

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import CSVLoader

from config.settings import (
                            PROCESSE_DATA_PATH,
                            DATASET_PATH, 
                            CSV_READING_ARGS
                            )

def save_vectore_database() -> None:
    print("TRYING TO CREATE VECTOR DATABASE")
    embeddings = OpenAIEmbeddings()

    loaded_docs = CSVLoader(PROCESSE_DATA_PATH, encoding="utf-8", csv_args=CSV_READING_ARGS).load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(loaded_docs)

    if os.path.isdir(DATASET_PATH):
        print("VECTOR DATABASE ALREADY EXISTS")
    else:
        db = FAISS.from_documents(docs, embeddings)
        db.save_local(DATASET_PATH)
        print("VECTOR DATABASE CREATED")