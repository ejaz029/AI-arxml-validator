import streamlit as st
import os
from ai.rag_validation import RAGValidator

def chatbot_interface(user_query, arxml_path):
    """Handles AI chatbot interactions for ARXML validation queries."""
    validator = RAGValidator(arxml_path)
    arxml_text = validator.load_arxml()

    if "Error" in arxml_text:
        return arxml_text

    validator.build_vector_db(arxml_text)
    validator.setup_rag_pipeline()

    response = validator.qa_chain.run(user_query)
    return response

# Streamlit UI for Chatbot
#st.set_page_config(page_title="ARXML Validator Chatbot", layout="wide")

st.title("🤖 ARXML Validator Chatbot")
st.write("Ask any ARXML-related question and get AI-powered insights!")

# Create an 'uploads' directory if it doesn't exist
upload_dir = "uploads"
os.makedirs(upload_dir, exist_ok=True)

uploaded_file = st.file_uploader("Upload your ARXML file", type=["arxml"])

if uploaded_file:
    arxml_path = os.path.join(upload_dir, uploaded_file.name)
    
    with open(arxml_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")

    user_query = st.text_input("🔍 Ask a question about your ARXML file:")
    if user_query:
        with st.spinner("Processing..."):
            response = chatbot_interface(user_query, arxml_path)  # Corrected function call
        st.markdown("### 🤖 AI Response:")
        st.write(response)
