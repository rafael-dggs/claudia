import os
from openai import AzureOpenAI
from flask import current_app

def classify_intent(last_message: str) -> str:
    """
    Analisa a mensagem do usuário e classifica a intenção em três categorias:
    - QUIZ: O usuário quer um teste, prova, simulado ou questões de avaliação.
    - CHAT: O usuário quer conversar, aprender um conceito ou tirar uma dúvida geral/documental.
    """
    endpoint = current_app.config.get('AZURE_AI_ENDPOINT')
    api_key = current_app.config.get('AZURE_AI_API_KEY')
    deployment_name = current_app.config.get('AZURE_AI_DEPLOYMENT_NAME', 'gpt-4o')

    system_prompt = """Você é um classificador de intenções roteador.
Analise a mensagem do usuário e responda APENAS com uma destas palavras em maiúsculo:
QUIZ - se o usuário pedir para criar questões, testes, avaliações ou exercícios.
CHAT - para qualquer outra requisição (dúvidas, explicações, resumos, conversa).
Não adicione pontuação ou texto adicional."""

    try:
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version="2024-02-15-preview"
        )

        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": last_message}
            ],
            max_completion_tokens=5
        )

        intent = response.choices[0].message.content.strip().upper()
        return intent if intent in ['QUIZ', 'CHAT'] else 'CHAT'
    except Exception as e:
        current_app.logger.error(f"Erro no Agente Supervisor: {e}")
        return 'CHAT'