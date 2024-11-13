from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory.buffer import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from django.conf import settings
import os
from dotenv import load_dotenv
from dotenv import dotenv_values
import shutil

load_dotenv()
config = dotenv_values(".env")

@api_view(['POST'])
@parser_classes([MultiPartParser])
def process_pdfs(request):
    pdf_files = request.FILES.getlist('pdfs')
    text = ""

    # Extract text from PDFs
    for pdf in pdf_files:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    
    # Split text into chunks
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200)
    text_chunks = text_splitter.split_text(text)
    # Create embeddings and vector store
    model_name = "sentence-transformers/all-mpnet-base-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)

    # Save vectorstore to disk or cache for query endpoint
    vectorstore_path = os.path.join(settings.BASE_DIR, "vector_store")
    vectorstore.save_local(vectorstore_path)
    # vectorstore.save_local("path/to/vectorstore")
    
    return Response({"message": "PDFs processed successfully."})



@api_view(["POST"])
def query_view(request):
    user_query = request.data.get("query")
    
    if not user_query:
        return Response({"error": "Query parameter is required."}, status=400)

    # Define the path to load vector store from BASE_DIR
    vectorstore_path = os.path.join(settings.BASE_DIR, "vector_store")
    if not os.path.exists(vectorstore_path):
        return Response({"error": "Vector store does not exist."}, status=404)
    # Load vector store
    model_name = "sentence-transformers/all-mpnet-base-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    try:
        vectorstore = FAISS.load_local(vectorstore_path, embeddings=embeddings,allow_dangerous_deserialization=True)
        
    except Exception as e:
        return Response({"error": f"Failed to load vector store: {str(e)}"}, status=500)

    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.5
    )

    # Set up conversation chain
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )

    # Get response
    try:
        response = conversation_chain({"question": user_query})
        return Response({"response": response['answer']})
    except Exception as e:
        return Response({"error": f"Failed to generate response: {str(e)}"}, status=500)
    

@api_view(["DELETE"])
def delete_vectorstore(request):
    # Define the path to the vector store directory
    vectorstore_path = os.path.join(settings.BASE_DIR, "vector_store")
    
    # Check if the vector store directory exists
    if os.path.exists(vectorstore_path):
        try:
            # Remove the entire vector store directory
            shutil.rmtree(vectorstore_path)
            return Response({"message": "Vector store deleted successfully."})
        except Exception as e:
            return Response({"error": f"Failed to delete vector store: {str(e)}"}, status=500)
    else:
        return Response({"error": "Vector store does not exist."}, status=404)