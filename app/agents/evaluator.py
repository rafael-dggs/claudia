import json
from openai import AzureOpenAI
from flask import current_app
from app.models.quiz import Quiz
from app import db

EVALUATOR_PROMPT = """Você é a ClaudIA em modo Avaliadora.
Sua única função é criar um questionário de múltipla escolha.
Você DEVE retornar APENAS um objeto JSON válido.
Estrutura EXATA do JSON:
{
  "topic": "Título do Assunto",
  "questions": [
    {
      "id": "q1",
      "text": "Pergunta?",
      "options": {"A": "Op 1", "B": "Op 2", "C": "Op 3", "D": "Op 4"},
      "correct": "A",
      "explanation": "Explicação correta"
    }
  ]
}"""

def generate_quiz_response(conversation_history: list, context_text: str, user_id: int) -> str:
    endpoint = current_app.config.get('AZURE_AI_ENDPOINT')
    api_key = current_app.config.get('AZURE_AI_API_KEY')
    deployment_name = current_app.config.get('AZURE_AI_DEPLOYMENT_NAME', 'gpt-4o')

    messages = [{"role": "system", "content": EVALUATOR_PROMPT}]
    if context_text:
        messages[0]["content"] += f"\n\n[CONTEXTO BASE PARA O QUIZ]:\n{context_text}"
        
    for msg in conversation_history:
        messages.append({"role": msg['sender'], "content": msg['content']})

    try:
        client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version="2024-02-15-preview")
        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            response_format={ "type": "json_object" }
        )
        
        raw_json = response.choices[0].message.content
        if not raw_json:
            return "Erro: A IA não conseguiu gerar o texto da prova."
            
        quiz_data = json.loads(raw_json)
        
        # Salva a prova na base de dados
        new_quiz = Quiz(user_id=user_id, topic=quiz_data.get('topic', 'Avaliação'), data=quiz_data)
        db.session.add(new_quiz)
        db.session.commit()
        
        # Devolve o botão HTML para abrir o modal
        return f"Preparei um questionário especial sobre o nosso assunto! Clique no botão abaixo para começar a prova.\n\n[QUIZ:{new_quiz.id}]"
        
    except json.JSONDecodeError:
        return "Desculpe, a IA não formatou as perguntas corretamente. Tente de novo."
    except Exception as e:
        current_app.logger.error(f"Erro Crítico no Avaliador: {e}")
        return "Tive um problema técnico ao comunicar com o Azure para preparar a sua prova."