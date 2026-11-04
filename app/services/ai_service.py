from flask import current_app
from app.rag.retrieval import retrieve_context
from app.agents.supervisor import classify_intent
from app.agents.professor import generate_teaching_response
from app.agents.evaluator import generate_quiz_response

def get_ai_response(conversation_history: list, user_id: int) -> str:
    """
    Orquestra a arquitetura multiagente:
    1. Recupera contexto vetorial (RAG).
    2. Classifica a intenção via Supervisor.
    3. Roteia para o Agente Professor ou Avaliador.
    """
    if not conversation_history:
        return "Olá! Como posso ajudar nos seus estudos hoje?"

    last_user_msg = conversation_history[-1]['content']

    # 1. Recuperação RAG (Independente da intenção, o documento apoia tanto ensino quanto quizzes)
    context_text = retrieve_context(query=last_user_msg, user_id=user_id)

    # 2. Supervisão / Classificação
    intent = classify_intent(last_user_msg)
    current_app.logger.info(f"Intenção detectada pelo Supervisor: {intent}")
    # Na função get_ai_response, localize o bloco try de roteamento e altere para:
    
    try:
        # 3. Roteamento Multiagente
        if intent == 'QUIZ':
            return generate_quiz_response(conversation_history, context_text, user_id)
        else:
            return generate_teaching_response(conversation_history, context_text)
        
    except Exception as e:
        current_app.logger.error(f"Falha na arquitetura multiagente: {e}")
        return "Desculpe, meus agentes enfrentaram uma instabilidade técnica. Pode tentar novamente?"