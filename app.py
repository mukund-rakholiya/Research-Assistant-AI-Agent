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
    st.header("Add Documents")
    # buttons to import documents
    if st.button("➕ Add PDF"):
        st.session_state.show_pdf_uploader = True
    
    if st.button("🔗 Add URL"):
        st.session_state.show_url_input = True
    
    # Show uploader if triggered
    if st.session_state.get("show_pdf_uploader", False):
        uploaded_pdf = st.file_uploader("Upload PDF", type="pdf")
        if uploaded_pdf:
            st.session_state.uploaded_pdfs = st.session_state.get("uploaded_pdfs", []) + [uploaded_pdf]
            st.session_state.show_pdf_uploader = False

    # Show URL input if triggered
    if st.session_state.get("show_url_input", False):
        url_input = st.text_input("Enter URL")
        if url_input:
            st.session_state.entered_urls = st.session_state.get("entered_urls", []) + [url_input]
            st.session_state.show_url_input = False
    
    st.divider()
    st.markdown("**Citation Style**")
    citation_style = st.radio("Format:", ["APA", "MAL"], horizontal = True)


# main content area
# Ensure session state lists exist
if "uploaded_pdfs" not in st.session_state:
    st.session_state.uploaded_pdfs = []
if "entered_urls" not in st.session_state:
    st.session_state.entered_urls = []
if "doc_ids" not in st.session_state:
    st.session_state.doc_ids = []
if "messages" not in st.session_state:
    st.session_state.messages = []

# Process and display all added documents
if st.session_state.uploaded_pdfs or st.session_state.entered_urls:

    st.subheader("📄 Processed Documents")
    with st.spinner("Analyzing documents..."):
        for uploaded_pdf in st.session_state.uploaded_pdfs:
            os.makedirs("uploads", exist_ok=True)
            file_path = os.path.join("uploads", uploaded_pdf.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_pdf.getbuffer())
            
            result = research_assistant(file_path, citation_style)
            if result["doc_id"] not in st.session_state.doc_ids:
                st.session_state.doc_ids.append(result["doc_id"])

            st.markdown(f"✅ **{uploaded_pdf.name}** processed.")
            st.markdown(result["summary"])
            st.code(result["citation"], language="text")

        for url in st.session_state.entered_urls:
            result = research_assistant(url, citation_style)
            st.session_state.doc_ids.append(result["doc_id"])
            st.markdown(f"🌐 **{url}** processed.")
            st.markdown(result["summary"])
            st.code(result["citation"], language="text")

    # Q&A section
    st.divider()
    st.subheader("💬 Ask Questions Across All Documents")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about any document..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Generating answer..."):
            combined_answer = ""
            for doc_id in st.session_state.doc_ids:
                answer = ask_question(prompt, doc_id)
                combined_answer += f"\n\n---\n📄 **Source:** {doc_id[:6]}\n{answer.content}"

        st.session_state.messages.append({"role": "assistant", "content": combined_answer})

        with st.chat_message("assistant"):
            st.markdown(combined_answer)

else:
    st.info("Use the sidebar to add PDFs or URLs to begin.")
