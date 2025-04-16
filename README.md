# 🚀 AI-Powered AUTOSAR ARXML Validator

## 📌 Project Overview
The **AI-Powered AUTOSAR ARXML Validator** is an advanced, modular, and scalable application designed to validate AUTOSAR `.arxml` files using both traditional rule-based logic and modern AI-powered techniques. The system helps engineers and developers detect data inconsistencies, structural issues, and anomalous patterns at node-level granularity.

## 💡 Key Features
- ✅ **UUID Validation:** Detects duplicate or missing UUIDs in AUTOSAR components.
- 🔗 **Reference Integrity Check:** Ensures that all references point to valid, existing elements.
- 🧩 **Attribute Presence & Format Validation:** Checks for mandatory attributes and correct formats.
- 🤖 **AI-powered Validation with RAG:** Integrates a Retrieval-Augmented Generation (RAG) pipeline to allow users to ask natural language queries about the validity and structure of ARXML files.
- 💬 **Chatbot Interface:** Offers an AI chatbot interface using Groq LLM for intelligent validation responses.
- 📊 **Streamlit UI:** Interactive and user-friendly web interface built with Streamlit.
- 🌐 **Cloud-Deployable:** Lightweight, modular, and ready for deployment to cloud platforms.

## 🧠 Tech Stack
| Component                  | Technology                     |
|---------------------------|----------------------------------|
| Frontend Interface        | Streamlit                        |
| AI Model Provider         | Groq (no `.env`, no OpenAI)      |
| AI Framework              | LangChain / LangGraph (RAG-based)|
| Backend Logic             | Python                           |
| ARXML Parsing             | xml.etree.ElementTree / lxml     |
| Deployment Target         | Cloud (Streamlit Share, etc.)    |

## 🗂️ Folder Structure
```
project-root/
│
├── config/                 # Configuration files (env, settings)
├── data/                   # Sample and uploaded ARXML files
├── validations/            # Validation modules (uuid.py, references.py, etc.)
├── ai/                     # AI logic (RAG pipeline, Groq interface)
├── streamlit_app/          # Streamlit frontend
├── utils/                  # Helper functions and common utilities
├── main.py                 # App entry point
└── README.md               # Project documentation
```

## 🧪 How to Run Locally
```bash
# 1. Clone the repository
$ git clone https://github.com/your-username/arxml-validator.git
$ cd arxml-validator

# 2. Install dependencies
$ pip install -r requirements.txt

# 3. Run the Streamlit app
$ streamlit run main.py
```

## 🔍 Validation Modules
Each validator is implemented as a separate Python module for clarity and scalability:
- `uuid_validator.py`
- `reference_validator.py`
- `attribute_validator.py`
- `anomaly_detector.py` (AI-enhanced)
- `rag_query_handler.py`

## 💬 Example Natural Language Queries
- "Are there any duplicate UUIDs?"
- "Do any software components reference missing elements?"
- "List all anomalies in communication stacks."
- "Is the ECU configuration complete?"

## 📈 Future Enhancements
- [ ] Integration with version control (e.g., Git hooks for validation)
- [ ] Real-time collaborative review tools
- [ ] Expanded AI reasoning for inter-node relationships

## 🙌 Contributors
- [Ejaz] – AI Integration, Project Lead
- [Teammate(not_yet)] – ARXML Parsing, Validation Logic

## 📄 License
MIT License

---
🧠 Built with AI + AUTOSAR ❤️

