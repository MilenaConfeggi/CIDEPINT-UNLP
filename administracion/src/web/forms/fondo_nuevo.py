from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Length, Optional, NumberRange
import re

class FormularioNuevoFondo(FlaskForm):
    def validar_solo_numeros(self, field):
        if not re.match(r"^\d+$", field.data):
            raise ValidationError("El campo solo puede contener números.")
        
    titulo = StringField('Titulo', validators=[DataRequired(message="es requerido"), 
                                             Length(max=50,message="no puede exceder los 50 caracteres")],
                       render_kw={"aria-label": "Titulo"}
                       )
    saldo = StringField('Saldo', validators=[DataRequired(message="es requerido"),
                                                  validar_solo_numeros],
                                                  render_kw={"aria-label": "Saldo"}
                                                  )