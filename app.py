import streamlit as st
from research_assistant import research_assistant, ask_question
import os

# configure page
st.set_page_config(
    page_title = "Research Assistant",
    layout = "wide"
)
st.title("📚 Smart Research Assistant")

# sidebar for input
with st.sidebar:
    st.header("Upload PDF")
    uploaded_file = st.file_uploader("Choose PDF", type = "pdf")
    url = st.text_input("Or enter URL (arXiv or article):")
    
    st.divider()
    st.markdown("**Citation Style**")
    citation_style = st.radio("Format:", ["APA", "MAL"], horizontal = True)

if uploaded_file or url:
    pass

else:
    st.info("Upload a PDF or enter URL to get started")