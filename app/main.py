# Copyright (c) 2025 Ejaz Belgaum
# Licensed under the MIT License (see LICENSE file for details).

import streamlit as st
import os
import sys
import xml.etree.ElementTree as ET
import xml.dom.minidom

# ✅ Set page config
st.set_page_config(page_title="AUTOSAR ARXML Validator & Chatbot", layout="wide")

# ✅ Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ✅ Imports
from ai.ai_chatbot import chatbot_interface
from app.file_utils import load_arxml_folder  # Note: bulk loader
from validators.schema_validation import validate_arxml_schema
from validators.data_consistency import validate_data

# ✅ Uploads folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def pretty_print_xml(root):
    """Returns pretty-printed XML string from ElementTree root."""
    xml_str = ET.tostring(root, encoding="utf-8")
    return xml.dom.minidom.parseString(xml_str).toprettyxml()

def main():
    st.title("🚗 AUTOSAR ARXML Validator & AI Chatbot")

    menu = ["Chatbot", "ARXML Validator", "Upload & View ARXML"]
    choice = st.sidebar.selectbox("🔍 Select Feature", menu)

    if choice == "Chatbot":
        chatbot_interface(upload_dir=UPLOAD_FOLDER)

    elif choice == "ARXML Validator":
        st.subheader("🛠️ ARXML File Validation")
        uploaded_file = st.file_uploader("📤 Upload ARXML File for Validation", type=["arxml"])
        if uploaded_file:
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ File uploaded: {uploaded_file.name}")

            xsd_schema_path = os.path.join(os.path.dirname(__file__), "..", "AUTOSAR_schema.xsd")
            is_valid, validation_errors = validate_arxml_schema(file_path, xsd_schema_path)

            if not is_valid:
                st.error("❌ Schema Validation Failed:")
                for err in validation_errors:
                    st.write(f"🔴 {err}")
            else:
                st.success("✅ ARXML file is valid!")

    elif choice == "Upload & View ARXML":
        st.subheader("📄 Upload ARXML File")
        uploaded_file = st.file_uploader("📤 Upload ARXML File", type=["arxml"])
        if uploaded_file:
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ File uploaded: {uploaded_file.name}")

        st.subheader("📂 View All ARXML Files in 'uploads/' Folder")
        arxml_data, failed_files = load_arxml_folder(UPLOAD_FOLDER)

        if not arxml_data and not failed_files:
            st.info("📭 No ARXML files found.")
        else:
            for filename, root in arxml_data:
                with st.expander(f"📄 {filename}"):
                    pretty_xml = pretty_print_xml(root)
                    st.code(pretty_xml, language="xml")

            if failed_files:
                st.error("❌ Failed to parse some files:")
                for filename, error_msg in failed_files:
                    st.write(f"🔴 {filename}: {error_msg}")

if __name__ == "__main__":
    main()
