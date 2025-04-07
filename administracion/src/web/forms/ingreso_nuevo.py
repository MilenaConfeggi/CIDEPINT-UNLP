from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, IntegerField, ValidationError, FileField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, Regexp
import re

class FormularioNuevoIngreso(FlaskForm):
    def validar_solo_numeros(self, field):
        if not re.match(r"^-?\d*(\.\d+)?$", field.data):
            raise ValidationError("El campo solo puede contener números.")
    monto = StringField('Monto', validators=[DataRequired(message="es requerido"),
                                                  validar_solo_numeros],
                                                  render_kw={"aria-label": "Monto"}
                                                  )
    file = FileField(
        "Archivo",
        validators=[
            #FileRequired(message="Debe seleccionar un archivo"),
            #Regexp(r'^[^/\\]+\.(pdf)$', message="Solo se permiten archivos PDF"),
        ],
    )