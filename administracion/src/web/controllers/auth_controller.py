from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models.base import db
from models.personal.personal import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            if not user.empleado.habilitado:
                flash('Usuario no habilitado', 'error')
                return redirect(url_for('auth.login'))
            login_user(user)
            if user.empleado.primer_login:
                return redirect(url_for('auth.cambiar_contrasena'))
            return redirect(url_for('auth.dashboard'))  # Cambia 'dashboard' por la ruta que desees
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'error')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('topicos.html')

@auth_bp.route('/cambiar_contrasena', methods=['GET', 'POST'])
@login_required
def cambiar_contrasena():
    if request.method == 'POST':
        nueva_contrasena = request.form.get('nueva_contrasena')
        confirmar_contrasena = request.form.get('confirmar_contrasena')
        
        if nueva_contrasena != confirmar_contrasena:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('auth.cambiar_contrasena'))
        
        current_user.set_password(nueva_contrasena)
        current_user.empleado.primer_login = False
        db.session.commit()
        flash('Contraseña cambiada con éxito', 'success')
        return redirect(url_for('auth.dashboard'))
    
    return render_template('cambiar_contrasena.html')