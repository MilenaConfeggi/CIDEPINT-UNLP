from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Por favor, inicia sesión para acceder a esta página.', 'error')
                return redirect(url_for('auth.login'))
            if current_user.empleado.rol not in roles:
                flash('No tienes permiso para acceder a esta página.', 'error')
                return redirect(url_for('home'))
            if current_user.empleado.primer_login:
                flash('Por favor, cambia tu contraseña antes de continuar.', 'warning')
                return redirect(url_for('auth.cambiar_contrasena'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator