from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.quiz import Quiz, QuizAttempt
from app import db

quizzes_bp = Blueprint('quizzes', __name__)

@quizzes_bp.route('/<int:quiz_id>', methods=['GET'])
@login_required
def get_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.user_id != current_user.id:
        return jsonify({'error': 'Acesso negado'}), 403
    
    # Remove o gabarito e a explicação antes de enviar ao frontend
    safe_data = {"topic": quiz.topic, "questions": []}
    for q in quiz.data.get("questions", []):
        safe_data["questions"].append({
            "id": q["id"],
            "text": q["text"],
            "options": q["options"]
        })
        
    return jsonify(safe_data)

@quizzes_bp.route('/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.user_id != current_user.id:
        return jsonify({'error': 'Acesso negado'}), 403

    answers = request.json.get('answers', {}) # Formato esperado: {"q1": "A", "q2": "C"}
    
    correct_count = 0
    total = len(quiz.data.get("questions", []))
    feedback = []

    # Processa a correção
    for q in quiz.data.get("questions", []):
        user_ans = answers.get(q["id"])
        is_correct = user_ans == q["correct"]
        if is_correct:
            correct_count += 1
        
        feedback.append({
            "question": q["text"],
            "user_answer": user_ans,
            "correct_answer": q["correct"],
            "is_correct": is_correct,
            "explanation": q["explanation"]
        })
    
    score = (correct_count / total) * 100 if total > 0 else 0
    
    # Salva o resultado
    attempt = QuizAttempt(quiz_id=quiz.id, user_id=current_user.id, score=score, feedback_data=feedback)
    db.session.add(attempt)
    db.session.commit()

    return jsonify({
        "status": "success",
        "score": score,
        "correct_count": correct_count,
        "total": total,
        "feedback": feedback
    })