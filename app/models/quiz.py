from app import db
from datetime import datetime

class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic = db.Column(db.String(255), nullable=False)
    data = db.Column(db.JSON, nullable=False) # Armazena as perguntas, opções e respostas da IA
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Quiz {self.id} - {self.topic}>'


class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    feedback_data = db.Column(db.JSON, nullable=False) # Histórico de erros/acertos
    created_at = db.Column(db.DateTime, default=datetime.utcnow)