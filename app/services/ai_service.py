import os
from openai import AzureOpenAI, OpenAI
from flask import current_app

CLANDIA_SYSTEM_PROMPT = """Você é a ClaudIA, uma professora virtual inteligente, acolhedora, paciente e didática.
Seu objetivo é auxiliar o aluno a aprender, compreender e aprofundar qualquer assunto solicitado.

DIRETRIZES PEDAGÓGICAS:
1. Explique conceitos progressivamente, dividindo assuntos complexos em etapas menores.
2. Utilize exemplos práticos, analogias e comparações claras do cotidiano.
3. Identifique dificuldades de entendimento implícitas e reformule explicações quando necessário.
4. Incentive o pensamento crítico e a autonomia do estudante, fazendo perguntas instigantes.
5. Mantenha um tom profissional, acolhedor e simpático, sem ser excessivamente formal ou exageradamente meloso.
6. Nunca invente informações factuais quando faltarem dados nas fontes (o que será expandido com RAG nas próximas fases). Seja transparente.
"""

def get_ai_response(conversation_history: list) -> str:
    """
    Envia o histórico da conversa para o modelo LLM configurado no Azure AI Foundry
    e retorna a resposta pedagógica da ClaudIA.
    """
    endpoint = current_app.config.get('AZURE_AI_ENDPOINT')
    api_key = current_app.config.get('AZURE_AI_API_KEY')
    deployment_name = current_app.config.get('AZURE_AI_DEPLOYMENT_NAME', 'gpt-4o')

    # Monta as mensagens estruturadas para a API
    messages = [{"role": "system", "content": CLANDIA_SYSTEM_PROMPT}]
    for msg in conversation_history:
        messages.append({
            "role": msg['sender'],  # 'user' ou 'assistant'
            "content": msg['content']
        })

    # Fallback caso as chaves do Azure não estejam configuradas no .env (para testes iniciais de UI)
    if not endpoint or not api_key or 'seu-recurso' in endpoint:
        # Resposta simulada inteligente para validação da interface e fluxo
        last_user_msg = conversation_history[-1]['content'] if conversation_history else ""
        return (
            f"Olá! Percebi que você perguntou sobre: *\"{last_user_msg}\"*. "
            "Como ainda estamos configurando as chaves oficiais do Azure AI Foundry no seu arquivo `.env`, "
            "esta é uma resposta simulada da minha personalidade pedagógica. "
            "Assim que você inserir suas credenciais reais do Azure, estarei conectada ao GPT para te ensinar "
            "com analogias, exemplos práticos e explicações passo a passo!"
        )

    try:
        # Inicialização do cliente Azure OpenAI
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version="2024-02-15-preview"
        )

        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            temperature=0.7,
            max_tokens=1500
        )

        return response.choices[0].message.content
    except Exception as e:
        current_app.logger.error(f"Erro ao comunicar com Azure AI Foundry: {str(e)}")
        return "Desculpe, tive um pequeno problema técnico ao consultar meus servidores de IA no Azure. Por favor, tente novamente em instantes."