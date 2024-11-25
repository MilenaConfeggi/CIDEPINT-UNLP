from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Length, Optional, NumberRange
import re

class FormularioNuevoIngreso(FlaskForm):
    def validar_solo_numeros(self, field):
        if not re.match(r"^\d+$", field.data):
            raise ValidationError("El campo solo puede contener números.")
    monto = StringField('Monto', validators=[DataRequired(message="es requerido"),
                                                  validar_solo_numeros],
                                                  render_kw={"aria-label": "Monto"}
                                                  )