from openai import AzureOpenAI
from flask import current_app

def get_embedding(text: str) -> list[float]:
    """
    Gera o vetor de embedding para um texto utilizando o Azure OpenAI.
    """
    endpoint = current_app.config['AZURE_AI_ENDPOINT']
    api_key = current_app.config['AZURE_AI_API_KEY']
    deployment_name = current_app.config['AZURE_AI_EMBEDDINGS_DEPLOYMENT_NAME']

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version="2023-05-15"
    )

    # Limpa quebras de linha excessivas que prejudicam a qualidade do vetor
    text = text.replace("\n", " ")
    
    response = client.embeddings.create(
        input=[text],
        model=deployment_name
    )
    
    return response.data[0].embedding