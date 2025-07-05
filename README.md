# ragasus-ai-assistant
RAGASUS is an AI-powered intelligent assistant designed to help you effortlessly understand and interact with your documents. 


---

## 🧠 Features

- 📄 PDF Upload & Parsing — Upload and extract content from PDFs automatically
- 🔗 RAG-based Q&A — Combines document retrieval with powerful language model
- 🧠 Local LLM (Ollama + Mistral) — Privacy-first, no cloud dependency
- 🧭 Chatbot Interface — Ask queries and get document-specific answers
- 📚 Vector Storage — Embedding-based retrieval using FAISS and LlamaIndex
- 🌐 Built with Streamlit for an interactive frontend.
- 🛠 Developer-friendly setup using `pipenv`.

---

## 🚀 Getting Started

### 1. Clone the Repository

```
git clone https://github.com/Vishal-Patoliya/ragasus-ai-assistant.git
```

### 2. Install Python Dependencies
Make sure you have pipenv installed. If not, install it:

```
pip install pipenv
```

Then install the dependencies:

```
pipenv install llama-index llama-index-llms-ollama llama-index-embeddings-ollama llama-index-vector-stores-faiss pymupdf
pipenv install streamlit langchain langchain_community langchain_ollama pypdf faiss-cpu
```

### 3. Set Up and Run Local LLM (via Ollama)
Install Ollama from https://ollama.com, then download the Mistral model:

```
ollama pull mistral
```

Make sure Ollama is running before starting the quiz builder.


### 4. Run the Application with Streamlit
Install Streamlit if needed:

```
pip install streamlit
```

Navigate to the frontend directory and start the app:

```
cd frontend
streamlit run main.py
```

### ✅ Requirements
```
Python 3.8 or later

pipenv

streamlit

Ollama (for running local LLMs)

Mistral model (ollama pull mistral)
```

## 🧑‍💼 Author
Vishal Patoliya

[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vishal-patoliya/)