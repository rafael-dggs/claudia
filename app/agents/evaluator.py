from openai import AzureOpenAI
from flask import current_app

EVALUATOR_PROMPT = """Você é a ClaudIA em modo Avaliadora.
Sua função é criar questões de múltipla escolha ou dissertativas para testar o conhecimento do aluno.

DIRETRIZES DO AVALIADOR:
1. Crie questões claras, desafiadoras e adequadas ao nível solicitado ou deduzido pela conversa.
2. Se um [CONTEXTO DOCUMENTAL] for fornecido, baseie as perguntas estritamente nele.
3. Formate a saída de forma organizada, utilizando markdown. Para múltipla escolha, liste as alternativas de A a D.
4. No final do questionário, pergunte educadamente se o aluno deseja tentar responder agora para que você possa corrigir."""

def generate_quiz_response(conversation_history: list, context_text: str = "") -> str:
    endpoint = current_app.config.get('AZURE_AI_ENDPOINT')
    api_key = current_app.config.get('AZURE_AI_API_KEY')
    deployment_name = current_app.config.get('AZURE_AI_DEPLOYMENT_NAME', 'gpt-4o')

    system_prompt = EVALUATOR_PROMPT
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
        return response.choices[0].message.content
    except Exception as e:
        current_app.logger.error(f"Erro no Agente Avaliador: {e}")
        raise e