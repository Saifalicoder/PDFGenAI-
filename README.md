# PDFGenAI

PDFGenAI is a powerful document processing and query application built using Django and LangChain. The project allows users to upload PDFs, process them to extract content, and then interact with the extracted data through conversational queries. It integrates various technologies such as FAISS vector store, Google Generative AI, and LangChain for natural language processing.

## Features

- **Upload PDF Files**: Users can upload multiple PDF files for processing.
- **Conversational Querying**: Users can ask questions based on the processed PDFs, with responses powered by AI and stored data.
- **API**: The backend exposes API endpoints for processing PDFs, querying, and managing the vector store.

## Technologies Used

- **Django**: Web framework for building the backend of the application.
- **LangChain**: Framework to build language model-driven applications.
- **FAISS**: Library for efficient similarity search and clustering of dense vectors.
- **HuggingFace Transformers**: For embedding generation used in vector search.
- **Google Generative AI (Gemini 1.5)**: Language model to generate responses based on user queries.
- **PyPDF2**: Python library for PDF text extraction.
- **Streamlit**: Frontend interface to interact with the backend.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Saifalicoder/PDFGenAI-.git
cd PDFGenAI-
```

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```
### Create .env files in project root
```bash
GOOGLE_API_KEY=your_google_api_key
HUGGINGFACEHUB_API_TOKEN=huggs_token
```

### Run django server
```bash
python manage.py runserver
```

### Run streamlit app
```bash
streamlit run app.py
```
