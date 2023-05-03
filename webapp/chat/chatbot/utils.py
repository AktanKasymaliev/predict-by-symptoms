from typing import List

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.vectorstores.base import VectorStoreRetriever

from config.settings import DATASET_PATH


def init_vector_retriever():
    embeddings = OpenAIEmbeddings()
    try:
        db = FAISS.load_local(DATASET_PATH, embeddings)
        return db.as_retriever(search_type="mmr")
    except Exception as e:
        raise Exception(
            "Could not load vector database. Please run `python manage.py create_vector_db`"
        )

def get_data_from_vectorstore(retriever: VectorStoreRetriever, question: str) -> List[tuple]:
    docs = retriever.get_relevant_documents(question)
    answers = [ans.page_content.split("\n")[1] for ans in docs]
    focuses = [ans.page_content.split("\n")[-1] for ans in docs]
    return [i for i in zip(answers, focuses)]