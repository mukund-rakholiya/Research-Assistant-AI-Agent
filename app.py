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
    # saving uploaded file
    if (uploaded_file):
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        input_source = file_path
    else :
        input_source = url
    
    # process document
    with st.spinner("Analyzing document..."):
        result = research_assistant(input_source, citation_style)
        print("DEBUG RESULT:", result)

    # display results
    st.subheader("Summary")
    st.markdown(result["summary"])
    
    st.subheader("Citation")
    st.code(result["citation"], language = "text")
    
    # Q & A section
    st.divider()
    st.subheader("Document Q&A")
    
    if ("messages" not in st.session_state):
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask about this document..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
    
        # adding the user's answer to the session
        with st.chat_message("user"):
            st.markdown(prompt)
    
else:
    st.info("Upload a PDF or enter URL to get started")