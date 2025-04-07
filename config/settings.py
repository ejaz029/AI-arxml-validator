import os
from langchain_groq import ChatGroq

class Config:
    """Configuration settings for the AUTOSAR Validator application."""

    # ✅ AI Model Configuration
    AI_PROVIDER = "groq"
    AI_MODEL = "mixtral-8x7b"  # You can change to llama3-8b-8192 or gemma-7b if needed

    # ✅ File Handling
    UPLOAD_FOLDER = "uploads"
    ALLOWED_EXTENSIONS = {"arxml"}

    # ✅ Validation Settings
    ENABLE_RAG_VALIDATION = True
    ENABLE_SCHEMA_CHECK = True
    ENABLE_CONSISTENCY_CHECKS = True

    # ✅ Load Groq API Key (from YAML or directly here)
    GROQ_API_KEY = "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"  # Replace with your real key or load from config.yaml

    # ✅ Deployment
    DEPLOYMENT_ENV = "local"

    @staticmethod
    def is_allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

# ✅ Attach LLM instance *after* class definition
Config.llm = ChatGroq(model_name=Config.AI_MODEL, groq_api_key=Config.GROQ_API_KEY)
