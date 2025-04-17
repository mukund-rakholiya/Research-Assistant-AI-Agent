import streamlit as st
from research_assistant import research_assistant, ask_question
import os

# configure page
st.set_page_config(
    page_title = "Research Assistant",
    layout = "wide"
)
st.title("📚 Smart Research Assistant")