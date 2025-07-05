import os
import faiss
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.readers.file import PyMuPDFReader

# === Paths ===
UPLOAD_DIR = "../uploaded_documents"   # folder where PDFs are uploaded
INDEX_DIR = "../document-index"        # folder where FAISS + metadata will be saved

# === Load and Process PDFs ===
def ingest_docs():
    try:
        # 1. Set up embedding + splitter
        embed_model = OllamaEmbedding(model_name="mistral")
        splitter = SentenceSplitter(chunk_size=600, chunk_overlap=50)

        # 2. Load all PDFs
        pdf_files = [os.path.join(UPLOAD_DIR, f) for f in os.listdir(UPLOAD_DIR) if f.endswith(".pdf")]
        all_nodes = []
        reader = PyMuPDFReader()

        for pdf_path in pdf_files:
            documents = reader.load(file_path=pdf_path)
            nodes = splitter.get_nodes_from_documents(documents)
            all_nodes.extend(nodes)

        print(f"📄 Loaded and chunked {len(pdf_files)} PDFs into {len(all_nodes)} chunks.")

        # 3. Build FAISS index
        dim = len(embed_model.get_text_embedding("test"))
        faiss_index = faiss.IndexFlatL2(dim)
        vector_store = FaissVectorStore(faiss_index=faiss_index)

        # 4. Set up full storage context (vector store + docstore + index metadata)
        storage_context = StorageContext.from_defaults(
            persist_dir=INDEX_DIR,
            docstore=SimpleDocumentStore(),
            index_store=SimpleIndexStore(),
            vector_store=vector_store
        )

        # 5. Build the index
        VectorStoreIndex(
            nodes=all_nodes,
            embed_model=embed_model,
            storage_context=storage_context
        )

        # Ensure the directory exists
        os.makedirs(INDEX_DIR, exist_ok=True)

        # 6. Save FAISS and metadata
        faiss.write_index(faiss_index, os.path.join(INDEX_DIR, "faiss.index"))
        storage_context.persist(persist_dir=INDEX_DIR)

        print("FAISS index + metadata saved to:", INDEX_DIR)
        return True

    except Exception as e:
        print(f"Ingestion failed: {e}")
        return False
