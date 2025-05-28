# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_community.document_loaders import TextLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.chains import RetrievalQA

# # ✅ Import only get_llm from the correct config
# from config.llm_config import get_llm

# import xml.etree.ElementTree as ET

# class RAGValidator:
#     def __init__(self, arxml_path):
#         self.arxml_path = arxml_path
#         self.vector_db = None
#         self.qa_chain = None

#     def load_arxml(self):
#         try:
#             tree = ET.parse(self.arxml_path)
#             root = tree.getroot()
#             return ET.tostring(root, encoding="utf-8").decode()
#         except Exception as e:
#             return f"⚠️ Error parsing ARXML: {str(e)}"

#     def build_vector_db(self, arxml_text):
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#         docs = text_splitter.split_text(arxml_text)

#         embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#         self.vector_db = FAISS.from_texts(docs, embeddings)

#     def setup_rag_pipeline(self):
#         retriever = self.vector_db.as_retriever()
#         llm = get_llm()  # ✅ Correct LLM getter
#         self.qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)

#     def validate_arxml(self):
#         arxml_text = self.load_arxml()
#         if "Error" in arxml_text:
#             return arxml_text

#         self.build_vector_db(arxml_text)
#         self.setup_rag_pipeline()

#         prompt = (
#             "Analyze this ARXML data for inconsistencies, missing elements, UUID uniqueness issues, "
#             "and any potential errors based on AUTOSAR standards. Provide a structured response."
#         )
#         return self.qa_chain.run(prompt)
import os
import xml.etree.ElementTree as ET
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from config.llm_config import get_llm
from validators.extract_ports import extract_ports_from_arxml


def find_file_from_query(user_query, file_list):
    """Try to extract a filename (like 'G') from the query and match it with the actual files."""
    for file in file_list:
        base = file.lower().replace(".arxml", "")
        if base in user_query.lower():
            return file
    return None


def check_duplicate_uuids(arxml_data):
    """Scan across all files for duplicate UUIDs."""
    uuid_map = {}
    duplicates = []

    for filename, xml_str in arxml_data.items():
        try:
            root = ET.fromstring(xml_str)
            for elem in root.iter():
                uuid = elem.attrib.get("UUID")
                if uuid:
                    if uuid in uuid_map:
                        duplicates.append((uuid, uuid_map[uuid], filename))
                    else:
                        uuid_map[uuid] = filename
        except Exception as e:
            continue

    return duplicates


def process_query_with_rag(user_query, upload_folder):
    try:
        # ✅ Step: Custom rule for port report
        if "report of all ports" in user_query.lower() and "g.arxml" in user_query.lower():
            file_path = os.path.join(upload_folder, "G.arxml")
            if not os.path.exists(file_path):
                return "❌ G.arxml not found in uploads folder."

            ports = extract_ports_from_arxml(file_path)
            if not ports or "error" in ports[0]:
                return f"❌ Error extracting ports: {ports[0].get('error', 'Unknown issue')}"

            p_ports = [p for p in ports if p['port_type'] == "P-PORT"]
            r_ports = [p for p in ports if p['port_type'] == "R-PORT"]

            report_lines = [
                f"📄 G.arxml – Port Summary Report:\n",
                f"🔷 Total Ports Found: {len(ports)}",
                f"   🔹 P-PORTs: {len(p_ports)}",
                f"   🔹 R-PORTs: {len(r_ports)}\n",
                 f"🔌 P-PORTs (Provided Interfaces):"
            ]

            for i, p in enumerate(p_ports, 1):
                report_lines.append(f"{i}. Name: {p['name']}\n   Interface: {p['interface']}")

            report_lines.append(f"\n🔌 R-PORTs (Required Interfaces):")
            for i, p in enumerate(r_ports, 1):
                report_lines.append(f"{i}. Name: {p['name']}\n   Interface: {p['interface']}")

            return "\n".join(report_lines)

        # ✅ Step 1: Load ARXML data
        arxml_data = {}
        loaded_files = []

        for f in os.listdir(upload_folder):
            if f.endswith(".arxml"):
                try:
                    file_path = os.path.join(upload_folder, f)
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                    xml_str = ET.tostring(root, encoding="utf-8").decode()
                    arxml_data[f] = xml_str
                    loaded_files.append(f)
                except Exception as e:
                    arxml_data[f] = f"⚠️ Failed to parse {f}: {e}"

        if not arxml_data:
            return "❌ No ARXML files found to analyze."

        # ✅ Step 2: Check for specific file mention in query
        target_file = find_file_from_query(user_query, loaded_files)

        # ✅ Step 3: Handle UUID duplication queries
        if "duplicate uuid" in user_query.lower():
            duplicates = check_duplicate_uuids(arxml_data)

            if not duplicates:
                return f"📂 Files Loaded: {', '.join(loaded_files)}\n\n✅ No duplicate UUIDs found across files."

            dup_text = "\n".join(
                [f"❌ Duplicate UUID '{uuid}' found in both '{f1}' and '{f2}'." for uuid, f1, f2 in duplicates]
            )
            return f"📂 Files Loaded: {', '.join(loaded_files)}\n\n📊 {dup_text}"

        # ✅ Step 4: Prepare text for RAG
        if target_file:
            context_text = arxml_data[target_file]
            arxml_texts = [f"--- {target_file} ---\n{context_text}"]
        else:
            arxml_texts = [f"--- {f} ---\n{txt}" for f, txt in arxml_data.items()]

        combined_text = "\n\n".join(arxml_texts)

        # ✅ Step 5: Chunking, Embedding, Vector Search
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.split_text(combined_text)

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cuda"}
        )
        vector_db = FAISS.from_texts(docs, embeddings)
        retriever = vector_db.as_retriever()

        # ✅ Step 6: Run LLM QA Chain
        llm = get_llm()
        qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)

        prompt = (
            f"The user wants to compare ARXML files: {', '.join(loaded_files)}.\n\n"
            f"Query: {user_query}"
        )

        result = qa_chain.run(prompt)
        return f"📂 Files Loaded: {', '.join(loaded_files)}\n\n📊 Answer: {result}"

    except Exception as e:
        return f"❌ Error during RAG validation: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python ai\\rag_validation.py <upload_folder> <query>")
    else:
        upload_folder = sys.argv[1]
        user_query = " ".join(sys.argv[2:])
        result = process_query_with_rag(user_query, upload_folder)
        print(result)

