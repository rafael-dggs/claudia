import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-fallback')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///claudia.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações Azure AI (preparação para fases seguintes)
    AZURE_AI_ENDPOINT = os.getenv('AZURE_AI_ENDPOINT')
    AZURE_AI_API_KEY = os.getenv('AZURE_AI_API_KEY')
    AZURE_AI_DEPLOYMENT_NAME = os.getenv('AZURE_AI_DEPLOYMENT_NAME', 'gpt-4o')