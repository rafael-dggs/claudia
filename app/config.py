import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-fallback')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///claudia.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Uploads
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limite de 16MB por arquivo
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
    
    # Credenciais Azure AI (LLM)
    AZURE_AI_ENDPOINT = os.getenv('AZURE_AI_ENDPOINT')
    AZURE_AI_API_KEY = os.getenv('AZURE_AI_API_KEY')
    AZURE_AI_DEPLOYMENT_NAME = os.getenv('AZURE_AI_DEPLOYMENT_NAME', 'gpt-4o')
    
    # Credenciais Azure AI Search e Embeddings (RAG)
    AZURE_SEARCH_ENDPOINT = os.getenv('AZURE_SEARCH_ENDPOINT')
    AZURE_SEARCH_API_KEY = os.getenv('AZURE_SEARCH_API_KEY')
    AZURE_SEARCH_INDEX_NAME = os.getenv('AZURE_SEARCH_INDEX_NAME', 'claudia-documents-index')
    AZURE_AI_EMBEDDINGS_DEPLOYMENT_NAME = os.getenv('AZURE_AI_EMBEDDINGS_DEPLOYMENT_NAME', 'text-embedding-ada-002')