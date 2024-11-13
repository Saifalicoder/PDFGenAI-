from django.urls import path
from .views import process_pdfs,query_view,delete_vectorstore
urlpatterns = [
    path('process_pdfs/', process_pdfs, name='process_pdfs'),
     path("query/", query_view, name="query_view"),
     path("delete_vectorstore/", delete_vectorstore, name="delete"),
]