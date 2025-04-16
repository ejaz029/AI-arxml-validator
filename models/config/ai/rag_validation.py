from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

# ✅ Import only get_llm from the correct config
from config.llm_config import get_llm

import xml.etree.ElementTree as ET

class RAGValidator:
    def __init__(self, arxml_path):
        self.arxml_path = arxml_path
        self.vector_db = None
        self.qa_chain = None

    def load_arxml(self):
        try:
            tree = ET.parse(self.arxml_path)
            root = tree.getroot()
            return ET.tostring(root, encoding="utf-8").decode()
        except Exception as e:
            return f"⚠️ Error parsing ARXML: {str(e)}"

    def build_vector_db(self, arxml_text):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.split_text(arxml_text)

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_db = FAISS.from_texts(docs, embeddings)

    def setup_rag_pipeline(self):
        retriever = self.vector_db.as_retriever()
        llm = get_llm()  # ✅ Correct LLM getter
        self.qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)

    def validate_arxml(self):
        arxml_text = self.load_arxml()
        if "Error" in arxml_text:
            return arxml_text

        self.build_vector_db(arxml_text)
        self.setup_rag_pipeline()

        prompt = (
            "Analyze this ARXML data for inconsistencies, missing elements, UUID uniqueness issues, "
            "and any potential errors based on AUTOSAR standards. Provide a structured response."
        )
        return self.qa_chain.run(prompt)
