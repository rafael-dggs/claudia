from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SimpleField, SearchableField, SearchField,
    SearchFieldDataType, VectorSearch, HnswAlgorithmConfiguration,
    VectorSearchProfile
)
from flask import current_app
from app.rag.embeddings import get_embedding
import uuid

def setup_index():
    """
    Verifica se o índice existe no Azure AI Search. Se não, cria com a estrutura necessária.
    """
    endpoint = current_app.config['AZURE_SEARCH_ENDPOINT']
    key = current_app.config['AZURE_SEARCH_API_KEY']
    index_name = current_app.config['AZURE_SEARCH_INDEX_NAME']

    if not endpoint or not key:
        current_app.logger.warning("Credenciais do Azure Search ausentes. Ignorando setup do índice.")
        return

    credential = AzureKeyCredential(key)
    index_client = SearchIndexClient(endpoint=endpoint, credential=credential)

    try:
        index_client.get_index(index_name)
        current_app.logger.info(f"Índice '{index_name}' já existe.")
    except Exception:
        # Se não existe, vamos criar o esquema
        fields = [
            SimpleField(name="id", type=SearchFieldDataType.String, key=True),
            SimpleField(name="user_id", type=SearchFieldDataType.String, filterable=True),
            SimpleField(name="document_id", type=SearchFieldDataType.String, filterable=True),
            SearchableField(name="content", type=SearchFieldDataType.String),
            SearchField(
                name="content_vector",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vector_search_dimensions=1536, # Padrão para ada-002 e small-3
                vector_search_profile_name="my-vector-profile"
            )
        ]

        vector_search = VectorSearch(
            algorithms=[HnswAlgorithmConfiguration(name="my-hnsw")],
            profiles=[VectorSearchProfile(name="my-vector-profile", algorithm_configuration_name="my-hnsw")]
        )

        index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search)
        index_client.create_index(index)
        current_app.logger.info(f"Índice vetorial '{index_name}' criado com sucesso!")

def index_document_chunks(chunks: list[str], user_id: int, document_id: str):
    """
    Gera embeddings para os chunks e os envia para o Azure AI Search.
    """
    endpoint = current_app.config['AZURE_SEARCH_ENDPOINT']
    key = current_app.config['AZURE_SEARCH_API_KEY']
    index_name = current_app.config['AZURE_SEARCH_INDEX_NAME']
    
    credential = AzureKeyCredential(key)
    search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)
    
    documents_to_upload = []
    for chunk in chunks:
        vector = get_embedding(chunk)
        documents_to_upload.append({
            "id": str(uuid.uuid4()),
            "user_id": str(user_id),
            "document_id": str(document_id),
            "content": chunk,
            "content_vector": vector
        })
        
    if documents_to_upload:
        search_client.upload_documents(documents=documents_to_upload)