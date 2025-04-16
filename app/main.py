# import streamlit as st
# import os
# import sys

# # ✅ Set page config first to prevent Streamlit errors
# st.set_page_config(page_title="AUTOSAR ARXML Validator & Chatbot", layout="wide")

# # ✅ Ensure Python finds the validators and AI directories
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# # ✅ Import necessary modules AFTER setting paths
# from ai.ai_chatbot import chatbot_interface
# from app.file_utils import load_arxml_file
# from validators.schema_validation import validate_arxml_schema
# from ai.rag_validation import RAGValidator
# from validators.data_consistency import validate_data

# # ✅ Ensure the "uploads" directory exists
# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# def main():
#     """Main function for Streamlit UI"""
#     st.title("🚗 AUTOSAR ARXML Validator & AI Chatbot")

#     menu = ["Chatbot", "ARXML Validator", "Upload & View ARXML"]
#     choice = st.sidebar.selectbox("🔍 Select Feature", menu)

#     if choice == "Chatbot":
#         st.subheader("🤖 AI Chatbot for ARXML")

#         uploaded_file = st.file_uploader("📤 Upload your ARXML file", type=["arxml"])
#         if uploaded_file:
#             file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
#             with open(file_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())
#             st.success(f"✅ File uploaded successfully: {uploaded_file.name}")

#             user_query = st.text_input("💬 Ask a question about your ARXML file:")
#             if user_query:
#                 with st.spinner("🔍 AI is analyzing..."):
#                     response = chatbot_interface(user_query, file_path)
#                 st.markdown("### 🤖 AI Response:")
#                 st.write(response)

#     elif choice == "ARXML Validator":
#         st.subheader("🛠️ ARXML File Validation")
#         uploaded_file = st.file_uploader("📤 Upload ARXML File for Validation", type=["arxml"])
#         if uploaded_file:
#             file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
#             with open(file_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())
#             st.success(f"✅ File uploaded successfully: {uploaded_file.name}")

#             # Run schema validation
#             validation_errors = validate_arxml_schema(file_path)
#             if validation_errors:
#                 st.error("❌ Validation Errors Found!")
#                 for err in validation_errors:
#                     st.write(f"🔴 {err}")
#             else:
#                 st.success("✅ ARXML file is valid!")

#     elif choice == "Upload & View ARXML":
#         st.subheader("📄 Upload & View ARXML File")
#         uploaded_file = st.file_uploader("📤 Upload ARXML File", type=["arxml"])
#         if uploaded_file:
#             file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
#             with open(file_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())
#             st.success(f"✅ File uploaded successfully: {uploaded_file.name}")

#             arxml_content = load_arxml_file(file_path)
#             st.text_area("📑 ARXML Content Preview", arxml_content, height=300)

# if __name__ == "__main__":
#     main()
import streamlit as st
import os
import sys

# ✅ Set page config first
st.set_page_config(page_title="AUTOSAR ARXML Validator & Chatbot", layout="wide")

# ✅ Add root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ✅ Imports
from ai.ai_chatbot import chatbot_interface
from app.file_utils import load_arxml_file
from validators.schema_validation import validate_arxml_schema
from validators.data_consistency import validate_data

# ✅ Ensure uploads folder exists
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def main():
    st.title("🚗 AUTOSAR ARXML Validator & AI Chatbot")

    menu = ["Chatbot", "ARXML Validator", "Upload & View ARXML"]
    choice = st.sidebar.selectbox("🔍 Select Feature", menu)

    if choice == "Chatbot":
        # ✅ Pass folder path (string) to chatbot
        chatbot_interface(upload_dir=UPLOAD_FOLDER)

    elif choice == "ARXML Validator":
        st.subheader("🛠️ ARXML File Validation")
        uploaded_file = st.file_uploader("📤 Upload ARXML File for Validation", type=["arxml"])
        if uploaded_file:
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ File uploaded successfully: {uploaded_file.name}")

            validation_errors = validate_arxml_schema(file_path)
            if validation_errors:
                st.error("❌ Validation Errors Found!")
                for err in validation_errors:
                    st.write(f"🔴 {err}")
            else:
                st.success("✅ ARXML file is valid!")

    elif choice == "Upload & View ARXML":
        st.subheader("📄 Upload & View ARXML File")
        uploaded_file = st.file_uploader("📤 Upload ARXML File", type=["arxml"])
        if uploaded_file:
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ File uploaded successfully: {uploaded_file.name}")
            arxml_content = load_arxml_file(file_path)
            st.text_area("📑 ARXML Content Preview", arxml_content, height=300)

if __name__ == "__main__":
    main()
