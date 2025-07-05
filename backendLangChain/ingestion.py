import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

# Folder paths
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../uploaded_documents")
INDEX_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../document-index")

def ingest_docs():
    embeddings = OllamaEmbeddings(model="mistral")

    # Load all PDF files
    pdf_files = [os.path.join(UPLOAD_DIR, f) for f in os.listdir(UPLOAD_DIR) if f.endswith(".pdf")]
    all_documents = []

    for pdf_file in pdf_files:
        loader = PyPDFLoader(pdf_file)
        documents = loader.load()
        all_documents.extend(documents)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    documents = text_splitter.split_documents(all_documents)

    #
    # for doc in documents:
    #     metadata = doc.metadata["source"]
    #     metadata = metadata.replace("langchain-docs", "<Replace With Unique Value for highlight>")
    #     doc.metadata.update({"source": metadata})

    print(f"Going to add {len(documents)} to Faiss")

    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(INDEX_DIR)
    print("***Loading to vectorstore done***")
    return True

if __name__ == "__main__":
    ingest_docs()