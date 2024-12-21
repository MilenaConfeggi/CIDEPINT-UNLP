from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, FieldList, FormField, TextAreaField, IntegerField, ValidationError, HiddenField, SelectField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
import re
from administracion.src.core.servicios import personal as servicio_personal

class FormularioPermiso(FlaskForm):
    user_id = SelectField('Usuario', choices=[], coerce=int, validators=[DataRequired()])
    permiso = SelectField('Permiso', choices=[('ver', 'Ver'), ('editar', 'Editar')], validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(FormularioPermiso, self).__init__(*args, **kwargs)
        self.user_id.choices = [(usuario.id, f"{usuario.empleado.nombre} {usuario.empleado.apellido} - {usuario.empleado.email}") for usuario in servicio_personal.listar_usuarios_personal()]

class FormularioNuevaCarpeta(FlaskForm):
        
    nombre = StringField('Nombre', validators=[DataRequired(message="es requerido"), 
                                             Length(max=255,message="no puede exceder los 255 caracteres")],
                       render_kw={"aria-label": "Titulo"}
                       )
    
    permisos = FieldList(FormField(FormularioPermiso), min_entries=0)

    def __init__(self, *args, **kwargs):
        super(FormularioNuevaCarpeta, self).__init__(*args, **kwargs)