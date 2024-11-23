from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, TextAreaField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Length, Optional, NumberRange
import re

class FormularioNuevaCarpeta(FlaskForm):
        
    nombre = StringField('Nombre', validators=[DataRequired(message="es requerido"), 
                                             Length(max=255,message="no puede exceder los 255 caracteres")],
                       render_kw={"aria-label": "Titulo"}
                       )
    
    usuarios = SelectMultipleField('Usuarios',coerce=int, validators=[Optional()], render_kw={"aria-label": "Usuarios"})
    
    def __init__(self, *args, **kwargs):
        super(FormularioNuevaCarpeta, self).__init__(*args, **kwargs)
        self.usuarios.choices = [(usuario['id'], f"{usuario['nombre']}") for usuario in [{'id': 1, 'nombre' : 'Roberto Carlos'}, {'id': 2, 'nombre' : 'Juan Gabriel'}, {'id': 3, 'nombre' : 'Luis Miguel'}]]
        #self.usuarios.choices = [(usuario.id, f"{usuario.nombre} {usuario.apellido}") for usuario in servicio_usuarios.listar_usuarios_empleados()]