import re
from openai import AzureOpenAI
from flask import current_app

def classify_intent(last_message: str) -> str:
    """
    Router Híbrido: Verifica palavras-chave primeiro (rápido e infalível).
    Usa o LLM do Azure apenas como fallback para pedidos ambíguos.
    """
    msg_lower = last_message.lower()
    
    # 1. Filtro Lexical de Alta Precisão (Garante o roteamento correto)
    keywords = r'\b(quiz|prova|questionário|questionario|simulado|teste|avaliação|avaliacao|questões|questoes)\b'
    if re.search(keywords, msg_lower):
        current_app.logger.info("ROTEAMENTO: 'QUIZ' detectado por palavra-chave.")
        return 'QUIZ'

    # 2. Fallback via Inteligência Artificial
    endpoint = current_app.config.get('AZURE_AI_ENDPOINT')
    api_key = current_app.config.get('AZURE_AI_API_KEY')
    deployment_name = current_app.config.get('AZURE_AI_DEPLOYMENT_NAME', 'gpt-4o')

    system_prompt = "Responda apenas QUIZ se o usuário pedir para ser testado, avaliado ou quiser perguntas. Caso contrário, responda CHAT."

    try:
        client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version="2024-02-15-preview")
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": last_message}
            ],
        )
        intent = response.choices[0].message.content.strip().upper()
        current_app.logger.info(f"ROTEAMENTO: IA decidiu '{intent}'")
        return 'QUIZ' if 'QUIZ' in intent else 'CHAT'
    except Exception as e:
        current_app.logger.error(f"Erro no LLM do Supervisor: {e}")
        return 'CHAT'