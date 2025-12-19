import numpy as np
import pickle
import os


class VectorStore:
    def __init__(self, dim, path="D:/llm_vector_store"):
        self.dim = dim

        # Ensure directory exists on D drive
        os.makedirs(path, exist_ok=True)

        self.file_path = os.path.join(path, "vectors.pkl")

        # Load existing vectors if present
        if os.path.exists(self.file_path):
            with open(self.file_path, "rb") as f:
                self.vectors, self.metadata = pickle.load(f)
        else:
            self.vectors = []
            self.metadata = []

    def add(self, embeddings, metadata):
        print("VECTOR STORE ADD:", len(embeddings), "embeddings")
        self.vectors.extend(embeddings)
        self.metadata.extend(metadata)
        self.save()

    def search(self, query_embedding, k=5):
        if not self.vectors:
            return []

        query = np.array(query_embedding)
        vectors = np.array(self.vectors)

        scores = np.dot(vectors, query) / (
            np.linalg.norm(vectors, axis=1) * np.linalg.norm(query)
        )

        top_k = np.argsort(scores)[-k:][::-1]
        return [self.metadata[i] for i in top_k]

    def save(self):
        with open(self.file_path, "wb") as f:
            pickle.dump((self.vectors, self.metadata), f)
