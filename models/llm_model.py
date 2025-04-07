import os
from langchain_core.chat_models import ChatGroq  # Import Groq Chat Model

class LLMModel:
    def __init__(self, model_name="llama3-70b", temperature=0.1):
        """
        Initializes the LLM model with the given parameters using Groq API.
        """
        self.model = ChatGroq(model_name=model_name, temperature=temperature, groq_api_key=os.getenv("GROQ_API_KEY"))

    def generate_response(self, prompt):
        """
        Generates a response based on the given prompt using the Groq model.
        """
        return self.model.predict(prompt)

# Example Usage
if __name__ == "__main__":
    llm = LLMModel()
    response = llm.generate_response("Explain the AUTOSAR RTE process.")
    print("🤖 LLM Response:")
    print(response)
