from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from io import BytesIO
from PyPDF2 import PdfWriter
import os
import shutil

class PDFProcessingTests(TestCase):

    def setUp(self):
        # Create a mock PDF file
        self.pdf_file = self.create_mock_pdf()
        self.client = APIClient()

    def create_mock_pdf(self):
        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf_writer._add_text('Test PDF content'))
        pdf_bytes = BytesIO()
        pdf_writer.write(pdf_bytes)
        pdf_bytes.seek(0)
        return pdf_bytes

    def test_process_pdfs(self):
        # Send a POST request with the mock PDF
        response = self.client.post(
            '/process_pdfs/', 
            data={'pdfs': self.pdf_file},
            format='multipart'
        )

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("PDFs processed successfully", response.data['message'])

        # Ensure that the vector store is created
        vectorstore_path = os.path.join(self.settings.BASE_DIR, 'vector_store')
        self.assertTrue(os.path.exists(vectorstore_path))


class QueryViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Assuming vectorstore is created before testing the query
        self.setup_vector_store()

    def setup_vector_store(self):
        # Mock the vector store creation (e.g., call process_pdfs before querying)
        # This could be done manually or via another test call to process_pdfs.
        pass

    def test_query_success(self):
        user_query = "What is the content of the first page?"
        response = self.client.post(
            '/query/', 
            data={'query': user_query},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("response", response.data)
        self.assertIsInstance(response.data["response"], str)

    def test_query_no_query(self):
        # Sending request without query
        response = self.client.post(
            '/query/', 
            data={},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Query parameter is required", response.data["error"])

