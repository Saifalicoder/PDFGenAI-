import streamlit as st
import requests

# Django API URLs
PROCESS_PDFS_URL = "http://localhost:8000/process_pdfs/"
QUERY_VIEW_URL = "http://localhost:8000/query/"
DELETE_VECTORSTORE_URL = "http://localhost:8000/delete_vectorstore/"


def delete_vector_store():
    try:
        response = requests.delete(DELETE_VECTORSTORE_URL)
        if response.status_code == 200:
            st.success("Vector store deleted successfully.")
        else:
            st.error(f"Error: {response.json().get('error')}")
    except Exception as e:
        st.error(f"Failed to connect to the API: {str(e)}")


def process_pdfs(uploaded_files):
    try:
        # Prepare files for upload
        files = [("pdfs", file) for file in uploaded_files]
        
        # Send PDF files to Django API for processing
        response = requests.post(PROCESS_PDFS_URL, files=files)
        
        if response.status_code == 200:
            st.success("PDFs processed successfully.")
        else:
            st.error(f"Failed to process PDFs: {response.json().get('error')}")
    except Exception as e:
        st.error(f"Failed to connect to the API: {str(e)}")


# Streamlit App Title
st.title("PDF Processing and Query App")

# Clear Vector Store
if st.button("Clear Vector Store"):
    delete_vector_store()

# Section 1: Upload PDFs
st.header("Upload PDFs for Processing")
uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

if st.button("Process PDFs") and uploaded_files:
    with st.spinner("Processing PDFs..."):
        process_pdfs(uploaded_files)

# Section 2: Query the Processed PDFs
st.header("Query the PDF Content")
user_query = st.text_input("Enter your question")

if st.button("Query") and user_query:
    with st.spinner("Getting response..."):
        response = requests.post(QUERY_VIEW_URL, json={"query": user_query})
    
    if response.status_code == 200:
        answer = response.json().get("response")
        
        st.write("Response:", answer)

    else:
        st.error(f"Failed to get response: {response.json().get('error')}")
