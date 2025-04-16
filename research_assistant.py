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
