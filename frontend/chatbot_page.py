import os
import streamlit as st
from backendLLamaIndex.core import run_llm

def chatbot_page():
    st.title("RAGASUS - AI Assistant")

    # Get the uploaded file path from session state
    file_path = st.session_state.get("uploaded_file_path", None)

    # Display the uploaded file name
    if file_path:
        st.info(f"Using document: {os.path.basename(file_path)}")

    # Option to reset and go back to upload page
    if st.button("Upload a new document"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state["page"] = "upload"  # Navigate back to upload page
        st.rerun()

    # Chatbot functionality
    prompt = st.text_input("Prompt", placeholder="Enter your query here.")

    if "user_prompt_history" not in st.session_state:
        st.session_state["user_prompt_history"] = []

    if "chat_answer_history" not in st.session_state:
        st.session_state["chat_answer_history"] = []

    if prompt:
        with st.spinner("Generating response..."):
            generated_response = run_llm(query=prompt)
            formatted_response = generated_response["result"]

            st.session_state["user_prompt_history"].append(prompt)
            st.session_state["chat_answer_history"].append(formatted_response)

    # Display chat history
    if st.session_state["chat_answer_history"]:
        for generated_response, user_query in zip(st.session_state["chat_answer_history"],
                                                  st.session_state["user_prompt_history"]):
            st.chat_message("user").write(user_query)
            st.chat_message("assistant").write(generated_response)
