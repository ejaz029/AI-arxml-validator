from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_llm():
    return ChatGroq(
        temperature=0.2,
        model_name="llama3-70b-8192",
        api_key=os.getenv("GROQ_API_KEY")  # ✅ Safe loading
    )
