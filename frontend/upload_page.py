import os
import shutil
import streamlit as st
from backendLLamaIndex.ingestion import ingest_docs

UPLOAD_DIR = "../uploaded_documents"

def recreate_upload_directory():
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR)

def upload_page():
    st.set_page_config(page_title="RAGASUS - AI Assistant", layout="centered")
    st.markdown("""
        <style>
            .title {
                font-size: 2.5em;
                font-weight: bold;
                color: #1F4E79;
                text-align: center;
                margin-bottom: 10px;
            }
            .subtitle {
                text-align: center;
                font-size: 1.2em;
                color: #4A4A4A;
                margin-bottom: 30px;
            }
            .stButton > button {
                background-color: #1F4E79;
                color: white;
                font-weight: 600;
                border-radius: 8px;
                padding: 0.6em 1.5em;
                margin-top: 20px;
            }
            .stFileUploader {
                border: 2px dashed #1F4E79;
                border-radius: 10px;
                padding: 1em;
                background-color: #F5F8FA;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="title">RAGASUS - AI Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">See through your documents with eagle-eyed intelligence.</div>', unsafe_allow_html=True)

    # File Upload Section
    if "uploading" not in st.session_state:
        st.session_state.uploading = False

    uploaded_file = st.file_uploader("📄 Upload your document and ask questions", type=["pdf"])

    submit_disabled = st.session_state.uploading

    if st.button("🚀 Submit", disabled=submit_disabled):
        if uploaded_file is not None:
            st.session_state.uploading = True
            st.rerun()
        else:
            st.error("Please upload a file before clicking Submit.")
            st.session_state.uploading = False

    if st.session_state.uploading and uploaded_file is not None:
        with st.spinner("⏳ Uploading and processing your document..."):
            recreate_upload_directory()
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Run ingestion synchronously and wait for result
            ingestion_success = ingest_docs()

        # After spinner block ends, check ingestion result
        if ingestion_success:
            st.session_state["uploaded_file_path"] = file_path
            st.session_state["page"] = "chatbot"
        else:
            st.error("Failed to ingest document. Please try again.")
            st.session_state.uploading = False

        st.rerun()

    # Footer
    st.markdown("---")
