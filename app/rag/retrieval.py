from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from flask import current_app
from app.rag.embeddings import get_embedding

def retrieve_context(query: str, user_id: int, top_k: int = 3) -> str:
    """
    Busca no banco vetorial as informações mais relevantes para a pergunta do usuário.
    Garante o isolamento filtrando exclusivamente pelo `user_id`.
    """
    endpoint = current_app.config.get('AZURE_SEARCH_ENDPOINT')
    key = current_app.config.get('AZURE_SEARCH_API_KEY')
    index_name = current_app.config.get('AZURE_SEARCH_INDEX_NAME')

    if not endpoint or not key:
        return ""

    try:
        credential = AzureKeyCredential(key)
        search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)

        # Transforma a pergunta do usuário em um vetor
        query_vector = get_embedding(query)
        vector_query = VectorizedQuery(vector=query_vector, k_nearest_neighbors=top_k, fields="content_vector")

        # Realiza a busca vetorial aplicando filtro de segurança por usuário
        results = search_client.search(
            search_text=None,
            vector_queries=[vector_query],
            filter=f"user_id eq '{user_id}'",
            top=top_k
        )

        context_chunks = [result['content'] for result in results]
        
        if not context_chunks:
            return ""
            
        return "\n\n---\n\n".join(context_chunks)
        
    except Exception as e:
        current_app.logger.error(f"Erro na recuperação vetorial: {e}")
        return ""