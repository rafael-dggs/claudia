from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

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

    # Registra Blueprints
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    # Rota raiz temporária ou principal
    from flask import render_template
    from flask_login import login_required

    @app.route('/')
    @login_required
    def index():
        return render_template('index.html')

    # Cria tabelas do banco de dados no contexto inicial se não existirem
    with app.app_context():
        db.create_all()

    return app