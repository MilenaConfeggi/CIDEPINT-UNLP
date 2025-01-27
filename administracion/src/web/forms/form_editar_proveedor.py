from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
import re

class form_editar_proveedor(FlaskForm):

    razon_social = StringField('razon social', validators=[DataRequired(
        message="Este campo es requerido"), Length(max=50)])
    contacto = StringField('contacto', validators=[DataRequired(
        message="Este campo es requerido")])