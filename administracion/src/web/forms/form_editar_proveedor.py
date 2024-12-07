from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
import re

class form_editar_proveedor(FlaskForm):

    def validar_telefono(self, field):
        telefono = str(field.data)
        if not re.match(r'^\d{8,15}$', telefono):
            raise ValidationError("El número de contacto debe tener entre 8 y 15 dígitos.")

    razon_social = StringField('razon social', validators=[DataRequired(
        message="Este campo es requerido"), Length(max=50)])
    contacto = IntegerField('contacto', validators=[DataRequired(
        message="Este campo es requerido"), validar_telefono])