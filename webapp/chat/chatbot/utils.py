from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# from config.settings import DATASET_PATH

DATASET_PATH = ""

def init_vector_retriever():
    embeddings = OpenAIEmbeddings()
    try:
        db = FAISS.load(DATASET_PATH, embeddings)
        return db.as_retriever(search_type="mmr")
    except:
        raise Exception(
            "Could not load vector database. Please run `python manage.py init_db`"
        )