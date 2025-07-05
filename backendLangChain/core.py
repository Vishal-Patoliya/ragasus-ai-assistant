import os

from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub

vector_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../document-index")

def run_llm(query: str):
    embeddings = OllamaEmbeddings(model="mistral")
    new_vector_store = FAISS.load_local(
        vector_db_path, embeddings, allow_dangerous_deserialization=True
    )

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    combine_docs_chain = create_stuff_documents_chain(
        OllamaLLM(model="mistral"), retrieval_qa_chat_prompt
    )
    retrieval_chain = create_retrieval_chain(
        new_vector_store.as_retriever(), combine_docs_chain
    )

    result = retrieval_chain.invoke(input={"input": query})
    new_result = {
        "query": result["input"],
        "result": result["answer"],
        "source_document": result["context"]
    }
    return new_result
