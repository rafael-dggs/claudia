from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat.index')) # <-- Alterado aqui
        
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Bem-vinda(o) de volta! A ClaudIA estava te esperando.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('chat.index')) # <-- Alterado aqui
        else:
            flash('E-mail ou senha inválidos. Verifique seus dados.', 'danger')
            
    return render_template('login.html', is_login=True)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chat.index'))
        
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if User.query.filter_by(email=email).first():
            flash('Este e-mail já está cadastrado no sistema.', 'warning')
            return redirect(url_for('auth.register'))
            
        new_user = User(name=name, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça login para começar.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('login.html', is_login=False)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sessão com segurança. Até breve!', 'info')
    return redirect(url_for('auth.login'))