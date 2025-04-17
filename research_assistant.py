# Importing all the dependancies
import os
from dotenv import load_dotenv
import hashlib
from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import pytesseract
from pdf2image import convert_from_path
import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Declaring all API keys
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT
os.environ["SERPER_API_KEY"] = SERPER_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Initializing components
# google embeddings created
embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001", google_api_key = GOOGLE_API_KEY)

vectorStore = Chroma(
    embedding_function = embeddings, 
    persist_directory = "./chroma.db"
)

gemini_llm = ChatGoogleGenerativeAI(
    model = "gemini-2.0-flash",
    temperature = 0.3,
    api_key = GOOGLE_API_KEY
)

groq_llm = ChatGroq(
    temperature = 0,
    model = "llama3-8b-8192"
)

# Core functions
# this method extracts text fom the pdf if "process_pdf" function is unale to do so
def ocr_fallback(file_path):
    """Use OCR when text extraction fails"""
    images = convert_from_path(file_path)
    return "\n".join([pytesseract.image_to_string(img) for img in images])

# This method retireves test fromthe pdf
def process_pdf(file_path):
    """Extract Text from PDF with OCR fallback"""
    try:
        text = "\n".join([page.extract_text() for page in PdfReader(file_path).pages])
        return text if text.strip() else ocr_fallback(file_path)

    except Exception as e:
        print(f"PDF Error: {e}")
        return ocr_fallback(file_path)

# this method generates summary using Gemini
def generate_summary(text):
    """Crete bullet-point summary using Gemini"""
    prompt = f"""Summarize this research in bullet points:
    - key findings
    - Methodology
    - Conclusions\n\n{text[:15000]}"""
    
    return gemini_llm.invoke(prompt).content

# this method stores the document in vector store / chroma-db
def store_document(text, source):
    """Split and store text in vector database"""
    # this line is used to create unique hash code for document
    doc_id = hashlib.md5(source.encode()).hexdigest()
    
    # spilt the text in to chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )
    
    # Ccreat  documents with metadata
    split_docs = splitter.create_documents([text])
    for doc in split_docs:
        doc.metadata["source"]  = source
        doc.metadata["doc_id"] = doc_id
    
    # store the chunks into chroma/vector-store
    vectorStore.add_documents(split_docs)
    
    return doc_id

# This method generates answer based on context using Groq
def ask_question(question, doc_id):
    """Answer question about stored documents"""
    docs = vectorStore.similarity_search(
        query = question,
        filter = {"doc_id": doc_id},
        k = 1
    )
    
    # checking if any documents were returned
    if not docs:
        return "No relevent documents found."
    
    context = "\n\n".join([d.page_content for d in docs])
    prompt = f"Answer based on context:\nQ: {question}\n Context: {context}"
    return groq_llm.invoke(prompt)

# extracts the data from the web-url
def load_webpage(input_path):
    """Load tet from a webpage given its URL"""
    try:
        # send a GET request to the URL
        response = requests.get(input_path)
        response.raise_for_status() # thi will raise an error for bas responses
        
        # this will pasrse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        
        # exract the text fom the webpage
        # can be customized to extract specific elements if needed
        text = soup.get_text(separator = "\n", strip = True)
        
        return text

    except Exception as e:
        print(f"Error fetching the webpage: {e}")
        return ""
    
# Main Workflow
def research_assistant(input_path, citation_style = None, question = None):
    """End-to-End processing pipeline"""
    try:
        # Input process
        text = process_pdf(input_path) if input_path.endswith(".pdf") else load_webpage(input_path)
        doc_id = store_document(text, input_path)
        
        # Generate output
        summary = generate_summary(text)
        citation = f"[{citation_style}] Citation for {input_path}"
        
        # Q & A if requested
        answer = None
        if question:
            answer = ask_question(question, doc_id)
            
            answer_content = answer.content

        return {
                "summary": summary,
                "citation": citation,
                "doc_id": doc_id,
                "answer": answer_content if answer else None
        }

    except Exception as e:
        print("Error in research_assistant:", e)
        return None
