from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app.services.document_service import allowed_file, process_and_index_upload
from app.models.chat import Message
from app import db

documents_bp = Blueprint('documents', __name__)

@documents_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado.'}), 400
        
    file = request.files['file']
    conversation_id = request.form.get('conversation_id')
    
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado.'}), 400
        
    if not conversation_id:
        return jsonify({'error': 'ID da conversa não fornecido.'}), 400
        
    if file and allowed_file(file.filename):
        try:
            # Orquestra a extração e indexação
            document = process_and_index_upload(file, current_user.id)
            
            # Adiciona uma mensagem de sistema/assistente confirmando a leitura
            success_msg = f"📄 Li o documento **{document.filename}** e guardei na minha memória! O que você gostaria de saber ou estudar sobre ele?"
            
            assistant_msg = Message(
                conversation_id=conversation_id, 
                sender='assistant', 
                content=success_msg
            )
            db.session.add(assistant_msg)
            db.session.commit()
            
            return jsonify({
                'status': 'success', 
                'filename': document.filename,
                'assistant_message': {
                    'content': assistant_msg.content,
                    'created_at': assistant_msg.created_at.strftime('%H:%M')
                }
            })
            
        except Exception as e:
            return jsonify({'error': f'Falha ao processar arquivo: {str(e)}'}), 500
            
    return jsonify({'error': 'Tipo de arquivo não permitido (Apenas PDF, DOCX, TXT).'}), 400