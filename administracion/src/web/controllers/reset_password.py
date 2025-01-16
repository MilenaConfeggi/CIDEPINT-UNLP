from flask import Blueprint, request, url_for, flash, redirect, render_template, current_app as app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from models.personal.personal import User
from models.personal.empleado import Empleado
from models.base import db  # Importa db para realizar operaciones en la base de datos

reset_bp = Blueprint("reset", __name__, url_prefix="/reset_password")

@reset_bp.route('/', methods=['GET', 'POST'])
def reset_password():
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    if request.method == 'POST':
        email = request.form['email']
        # Verificar si el email existe en la base de datos
        empleado = Empleado.query.filter_by(email=email).first()
        if not empleado:
            flash('Email not found.', 'danger')
            return redirect(url_for('reset.reset_password'))
        
        user = empleado.user
        if not user:
            flash('No existe un usuario con la dirección de correo electrónico ingresada.', 'danger')
            return redirect(url_for('reset.reset_password'))

        token = s.dumps(email, salt='password-reset-salt')
        link = url_for('reset.reset_with_token', token=token, _external=True)
        msg = Message('Solicitud de cambio de contraseña', sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[email])
        msg.body = f'Tu link para resetear tu contraseña es: {link}'
        mail = app.extensions.get('mail')  # Obtén la instancia de Mail desde la aplicación
        mail.send(msg)
        flash('Un link para cambiar tu contraseña ha sido enviado a tu dirección de correo electrónico.', 'info')
        return redirect(url_for('auth.login'))  # Cambia 'login' por 'auth.login'
    return render_template('reset_password.html')

@reset_bp.route('/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('El link es invalido o expiró.', 'danger')
        return redirect(url_for('reset.reset_password'))
    
    empleado = Empleado.query.filter_by(email=email).first()
    if not empleado:
        flash('Dirección de correo electrónico invalida.', 'danger')
        return redirect(url_for('reset.reset_password'))
    
    user = empleado.user
    if not user:
        flash('No existe un usuario asociado con esta dirección de correo electrónico.', 'danger')
        return redirect(url_for('reset.reset_password'))

    if request.method == 'POST':
        new_password = request.form['password']
        user.set_password(new_password)  # Usa el método set_password para hashear la contraseña
        db.session.commit()
        flash('Tu contraseña ha sido actualizada con éxito.', 'success')
        return redirect(url_for('auth.login'))  # Cambia 'login' por 'auth.login'
    
    return render_template('reset_with_token.html', token=token)