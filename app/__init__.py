from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar a ClaudIA.'
login_manager.login_message_category = 'info'

def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa extensões
    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    # Importa modelos
    from app.models.user import User
    from app.models.chat import Conversation, Message
    from app.models.document import Document # NOVO

    # Registra Blueprints
    from app.routes.auth import auth_bp
    from app.routes.chat import chat_bp
    from app.routes.documents import documents_bp # NOVO
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(documents_bp, url_prefix='/docs') # NOVO
# (...)
# Cria tabelas do banco de dados e configura o banco vetorial
    with app.app_context():
        db.create_all()
        try:
            from app.rag.vector_store import setup_index
            setup_index()
        except Exception as e:
            app.logger.warning(f"Não foi possível inicializar o índice vetorial: {e}")

    return app
