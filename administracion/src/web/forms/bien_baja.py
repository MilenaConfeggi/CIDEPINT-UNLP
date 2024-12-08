from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Length

class FormularioBajaBien(FlaskForm):
    motivo_baja = TextAreaField('Motivo de baja', validators=[DataRequired(message="es requerido"), 
                                             Length(max=200,message="no puede exceder los 200 caracteres")],
                       render_kw={"aria-label": "Motivo de baja"}
                       )