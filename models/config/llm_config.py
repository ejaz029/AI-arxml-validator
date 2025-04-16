from langchain_groq import ChatGroq

def get_llm():
    return ChatGroq(
        temperature=0.2,
        model_name="llama3-70b-8192",
        api_key="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"  # ⛔ Keep this private in production
    )
