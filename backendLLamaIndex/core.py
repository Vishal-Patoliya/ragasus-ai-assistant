import os
import faiss
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core.query_engine import RetrieverQueryEngine

INDEX_DIR = "../document-index"
llm = Ollama(model="mistral")
embedding_model = OllamaEmbedding(model_name="mistral")

def run_llm(query: str):
    # Step 1: Load FAISS index from file
    faiss_index = faiss.read_index(os.path.join(INDEX_DIR, "faiss.index"))
    vector_store = FaissVectorStore(faiss_index=faiss_index)

    # Step 2: Load storage context with FAISS + docstore + metadata
    storage_context = StorageContext.from_defaults(
        persist_dir=INDEX_DIR,
        vector_store=vector_store
    )

    # Step 3: Load LlamaIndex index
    index = load_index_from_storage(storage_context, embed_model=embedding_model)

    # Step 4: Setup retriever and query engine
    retriever = index.as_retriever(similarity_top_k=3)
    query_engine = RetrieverQueryEngine.from_args(retriever=retriever, llm=llm)

    # Step 5: Query
    response = query_engine.query(query)

    return {
        "query": query,
        "result": str(response),
        "source_document": [node.node.get_content() for node in response.source_nodes]
    }
