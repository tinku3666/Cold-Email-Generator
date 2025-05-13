import os
import pandas as pd
import chromadb
import uuid

class Portfolio:
    def __init__(self, file_path=None):
        # Use default relative path if not provided
        if file_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, "resource", "my_portfolio.csv")

        self.file_path = file_path

        # Check if file exists
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"CSV file not found at path: {self.file_path}")

        # Load data
        self.df = pd.read_csv(self.file_path)
        self.data = self.df.copy()

        # Initialize ChromaDB persistent client
        self.chroma_client = chromadb.PersistentClient(path="vectorstore")
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.df.iterrows():
                self.collection.add(
                    documents=[row["Techstack"]],
                    metadatas=[{"links": row["Links"]}],
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        result = self.collection.query(query_texts=skills, n_results=2)
        return result.get('metadatas', [])
