import os

from django.core.management.base import BaseCommand, CommandError

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import CSVLoader

from config.settings import (
                            PROCESSE_DATA_PATH,
                            DATASET_PATH, 
                            CSV_READING_ARGS
                            )

class Command(BaseCommand):
    help = "Create vector database"

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO("INFO: Creating vector database"))
        embeddings = OpenAIEmbeddings()

        try:
            loaded_docs = CSVLoader(PROCESSE_DATA_PATH, encoding="utf-8", csv_args=CSV_READING_ARGS).load()
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            docs = text_splitter.split_documents(loaded_docs)
        except FileNotFoundError:
            raise CommandError("Processed data not found.")

        if os.path.isdir(DATASET_PATH):
            self.stdout.write(self.style.SUCCESS("SUCCESS: Vector database already exists"))
        else:
            db = FAISS.from_documents(docs, embeddings)
            db.save_local(DATASET_PATH)
            self.stdout.write(self.style.SUCCESS("SUCCESS: Vector database created"))