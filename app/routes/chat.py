from flask import Blueprint, render_template, redirect, url_for, request, jsonify, abort
from flask_login import login_required, current_user
from app import db
from app.models.chat import Conversation, Message
from app.services.ai_service import get_ai_response

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/')
@login_required
def index():
    # Busca todas as conversas do usuário ordenadas da mais recente para a mais antiga
    conversations = Conversation.query.filter_by(user_id=current_user.id).order_by(Conversation.created_at.desc()).all()
    
    active_conversation = None
    messages = []
    
    if conversations:
        active_conversation = conversations[0]
        messages = Message.query.filter_by(conversation_id=active_conversation.id).order_by(Message.created_at.asc()).all()
        
    return render_template('chat.html', 
                           conversations=conversations, 
                           active_conversation=active_conversation, 
                           messages=messages)

@chat_bp.route('/conversation/<int:conversation_id>')
@login_required
def get_conversation(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)
    if conversation.user_id != current_user.id:
        abort(403)
        
    conversations = Conversation.query.filter_by(user_id=current_user.id).order_by(Conversation.created_at.desc()).all()
    messages = Message.query.filter_by(conversation_id=conversation.id).order_by(Message.created_at.asc()).all()
    
    return render_template('chat.html', 
                           conversations=conversations, 
                           active_conversation=conversation, 
                           messages=messages)

@chat_bp.route('/conversation/new', methods=['POST'])
@login_required
def new_conversation():
    title = request.form.get('title', 'Nova Conversa de Estudo')
    conversation = Conversation(user_id=current_user.id, title=title[:50])
    db.session.add(conversation)
    db.session.commit()
    return redirect(url_for('chat.get_conversation', conversation_id=conversation.id))

@chat_bp.route('/conversation/<int:conversation_id>/send', methods=['POST'])
@login_required
def send_message(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)
    if conversation.user_id != current_user.id:
        return jsonify({'error': 'Acesso negado'}), 403
        
    data = request.get_json()
    user_content = data.get('message', '').strip()
    
    if not user_content:
        return jsonify({'error': 'Mensagem vazia'}), 400
        
    # 1. Salva a mensagem do usuário
    user_msg = Message(conversation_id=conversation.id, sender='user', content=user_content)
    db.session.add(user_msg)
    
    # Atualiza o título da conversa com base na primeira mensagem se ainda for o padrão
    if conversation.title == 'Nova Conversa' or conversation.title == 'Nova Conversa de Estudo':
        conversation.title = user_content[:40] + ('...' if len(user_content) > 40 else '')
        
    db.session.commit()
    
    # 2. Recupera o histórico completo para contexto da IA
    past_messages = Message.query.filter_by(conversation_id=conversation.id).order_by(Message.created_at.asc()).all()
    history = [{'sender': m.sender, 'content': m.content} for m in past_messages]
    
    # 3. Obtém a resposta da ClaudIA via Azure AI Foundry
    ai_response_text = get_ai_response(history)
    
    # 4. Salva a resposta da assistente
    assistant_msg = Message(conversation_id=conversation.id, sender='assistant', content=ai_response_text)
    db.session.add(assistant_msg)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'user_message': {
            'content': user_msg.content,
            'created_at': user_msg.created_at.strftime('%H:%M')
        },
        'assistant_message': {
            'content': assistant_msg.content,
            'created_at': assistant_msg.created_at.strftime('%H:%M')
        },
        'conversation_title': conversation.title
    })