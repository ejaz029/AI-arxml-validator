from langchain_groq import ChatGroq

def get_llm():
    return ChatGroq(
        temperature=0.2,
        model_name="llama3-70b-8192",
        api_key="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"  # ⛔ Keep this private in production
    )
