from openai import AzureOpenAI
from flask import current_app

PROFESSOR_PROMPT = """Você é a ClaudIA, uma professora virtual inteligente, paciente e didática.

DIRETRIZES DO PROFESSOR:
1. Explique conceitos progressivamente, dividindo assuntos complexos em etapas menores.
2. Utilize exemplos práticos, analogias e comparações claras do cotidiano.
3. Se um [CONTEXTO DOCUMENTAL] for fornecido abaixo, utilize-o como base primária para a resposta.
4. Mantenha um tom acolhedor e encorajador."""

def generate_teaching_response(conversation_history: list, context_text: str = "") -> str:
    endpoint = current_app.config.get('AZURE_AI_ENDPOINT')
    api_key = current_app.config.get('AZURE_AI_API_KEY')
    deployment_name = current_app.config.get('AZURE_AI_DEPLOYMENT_NAME', 'gpt-4o')

    system_prompt = PROFESSOR_PROMPT
    if context_text:
        system_prompt += f"\n\n[CONTEXTO DOCUMENTAL RECUPERADO]:\n{context_text}"

    messages = [{"role": "system", "content": system_prompt}]
    for msg in conversation_history:
        messages.append({"role": msg['sender'], "content": msg['content']})

    try:
        client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version="2024-02-15-preview")
        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            max_completion_tokens=1500
        )
        
        # Proteção contra respostas vazias ou nulas da API
        content = response.choices[0].message.content
        if not content or not content.strip():
            return "Desculpe, a IA gerou uma resposta vazia. Pode reformular a pergunta?"
            
        return content
    except Exception as e:
        current_app.logger.error(f"Erro no Agente Professor: {e}")
        raise e