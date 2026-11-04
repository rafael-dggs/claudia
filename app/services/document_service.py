import os
import fitz  # PyMuPDF
import docx
from werkzeug.utils import secure_filename
from flask import current_app
from app import db
from app.models.document import Document
from app.rag.chunking import chunk_text
from app.rag.vector_store import index_document_chunks

def allowed_file(filename: str) -> bool:
    allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def extract_text(file_path: str, filename: str) -> str:
    """Extrai texto bruto de PDFs, DOCX ou TXT."""
    ext = filename.rsplit('.', 1)[1].lower()
    text = ""
    
    try:
        if ext == 'pdf':
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text()
        elif ext == 'docx':
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif ext == 'txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
    except Exception as e:
        current_app.logger.error(f"Erro ao extrair texto de {filename}: {e}")
        raise e

    return text

def process_and_index_upload(file, user_id: int) -> Document:
    """Salva o arquivo, extrai texto, divide em chunks e envia para o Azure AI Search."""
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, f"{user_id}_{filename}")
    file.save(file_path)

    # Cria o registro no banco de dados
    new_doc = Document(user_id=user_id, filename=filename, file_path=file_path, status='processing')
    db.session.add(new_doc)
    db.session.commit()

    try:
        # 1. Extração de texto
        raw_text = extract_text(file_path, filename)
        
        if not raw_text.strip():
            raise ValueError("O documento está vazio ou não possui texto legível.")

        # 2. Chunking (Fase 3)
        chunks = chunk_text(raw_text)

        # 3. Embeddings e Indexação Vetorial (Fase 3)
        index_document_chunks(chunks=chunks, user_id=user_id, document_id=str(new_doc.id))

        # Atualiza status para sucesso
        new_doc.status = 'indexed'
        db.session.commit()
        return new_doc

    except Exception as e:
        new_doc.status = 'error'
        db.session.commit()
        current_app.logger.error(f"Falha na indexação do documento {filename}: {str(e)}")
        raise e