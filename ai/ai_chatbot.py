# Copyright (c) 2025 Ejaz Belgaum
# Licensed under the MIT License (see LICENSE file for details).


import os
import streamlit as st
from ai.rag_validation import process_query_with_rag 
from app.file_utils import load_arxml_file

def chatbot_interface(upload_dir="uploads"):
    st.subheader("🤖 AI Chatbot for ARXML")
    
    # Get all ARXML files in the uploads directory
    arxml_files = [f for f in os.listdir(upload_dir) if f.endswith(".arxml")]
    
    if not arxml_files:
        st.warning("⚠️ No ARXML files found in the uploads folder.")
        return

    # File selection dropdown
    selected_file = st.selectbox("📂 Select ARXML File", arxml_files)

    # Show confirmation of selected file
    selected_path = os.path.join(upload_dir, selected_file)
    st.success(f"✅ Using preloaded file: {selected_file}")

    # # Optional preview
    # with st.expander("📖 Preview selected file content"):
    #     content = load_arxml_file(selected_path)
    #     st.text_area("🧾 ARXML Content", content, height=300)

    # Ask user for input
    st.markdown("### 🔍 Ask a question about the ARXML file:")
    default_message = "💬 How can I help you? (Please type your ARXML-related question below)"
    user_query = st.text_input(default_message)

    # Handle response
    if user_query:
        with st.spinner("🤖 AI is thinking..."):
            # Load ALL ARXML files for context, not just selected
            arxml_data = {
                filename: load_arxml_file(os.path.join(upload_dir, filename))
                for filename in arxml_files
            }
            response = process_query_with_rag(user_query, upload_dir)
        st.markdown("### 🤖 AI Response:")
        st.write(response)
# response = process_query_with_rag(user_query, upload_dir)  # ✅ Correct
