from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField

class DownloadForm(FlaskForm):
    documento_id = HiddenField("ID del documento")
    submit = SubmitField("Descargar")