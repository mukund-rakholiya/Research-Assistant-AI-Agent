# 🧠 Research Assistant AI Agent

A powerful and lightweight AI-powered research assistant that can:
- Extract and summarize content from **PDFs or web pages**
- Store and manage documents in a **vector database**
- Allow **interactive question-answering** over the content using state-of-the-art LLMs (Gemini & LLaMA3)
- Provide **citations** in your chosen format (APA, MAL)

Built using [LangChain](https://www.langchain.com/), [Streamlit](https://streamlit.io/), Google Gemini, and Groq’s LLaMA3.

---

## 🚀 Features

- 📄 **Upload PDFs** or 🌐 **Paste URLs** to analyze research papers and online content
- ✂️ Automatic **OCR fallback** for scanned PDFs
- 🧠 **LLM summarization** using Gemini
- 📚 **Vector store (ChromaDB)** for long-term document storage and similarity search
- ❓ Ask **follow-up questions** and get contextual answers via Groq's LLaMA3
- 🔖 Auto-generate **citations** for each document

---

## 🛠️ Installation

```bash
git clone https://github.com/yourusername/Research-Assistant-AI-Agent.git
cd Research-Assistant-AI-Agent
pip install -r requirements.txt
```

---

## 🔑 Environment Setup

Create a `.env` file in the project root with your API keys:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
LANGCHAIN_PROJECT=your_langchain_project
SERPER_API_KEY=your_serper_api_key
GROQ_API_KEY=your_groq_api_key
```

---

## 💻 How to Run

To launch the web app:

```bash
streamlit run app.py
```

Then, open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧩 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python, LangChain
- **LLMs**: Google Gemini (`gemini-2.0-flash`) and Groq’s LLaMA3 (`llama3-8b-8192`)
- **Vector DB**: Chroma
- **OCR**: Tesseract
- **PDF Parsing**: PyPDF, pdf2image
- **Web Scraping**: BeautifulSoup

---

## 📁 Project Structure

```
├── app.py                      # Streamlit frontend
├── research_assistant.py      # Core processing logic
├── requirements.txt
└── .env                       # (User-created) API key configuration
```

---

## 🧠 Usage Example

1. Upload a PDF or provide a URL
2. The system processes and stores the content
3. View the generated summary and citation
4. Ask questions about any uploaded document in the chat interface

---

## 🧪 Sample Prompt

> "What are the key findings of the uploaded research paper?"
> 
> *(The assistant responds with a summarized answer, sourced from the closest matching document.)*

---

## 📌 Citation Styles Supported

- APA  
- MAL

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributions

Pull requests and issues are welcome! If you'd like to contribute, feel free to fork this repo and open a PR.

---

## ✨ Acknowledgements

- [LangChain](https://www.langchain.com/)
- [Google Generative AI](https://ai.google.dev/)
- [Groq](https://groq.com/)
- [Streamlit](https://streamlit.io/)
