from langchain_huggingface import HuggingFaceEmbeddings  # Free embeddings
from langchain.vectorstores import FAISS

class EmbeddingModel:
    def __init__(self):
        """Initialize the embedding model using OpenAI."""
        self.embeddings = HuggingFaceEmbeddings()
        self.vector_db = None

    def build_vector_db(self, texts):
        """
        Creates a FAISS vector database from a list of text chunks.
        """
        self.vector_db = FAISS.from_texts(texts, self.embeddings)

    def retrieve_similar_texts(self, query, top_k=3):
        """
        Retrieves the top-k most similar ARXML text chunks based on query.
        """
        if not self.vector_db:
            return ["⚠️ Vector database is not initialized."]
        
        docs = self.vector_db.similarity_search(query, k=top_k)
        return [doc.page_content for doc in docs]

# Example Usage
if __name__ == "__main__":
    model = EmbeddingModel()
    
    sample_texts = [
        "ARXML defines software components in an ECU.",
        "P-PORT and R-PORT must have matching data types.",
        "UUIDs must be unique for each entity.",
    ]
    
    model.build_vector_db(sample_texts)
    results = model.retrieve_similar_texts("Check UUID uniqueness.")
    
    print("🔍 Similar Texts Found:")
    for res in results:
        print(f"- {res}")
