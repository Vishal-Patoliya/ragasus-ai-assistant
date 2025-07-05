import streamlit as st
from upload_page import upload_page
from chatbot_page import chatbot_page

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state["page"] = "upload"  # Default to the upload page

# Navigation logic
if st.session_state["page"] == "upload":
    upload_page()
elif st.session_state["page"] == "chatbot":
    chatbot_page()
