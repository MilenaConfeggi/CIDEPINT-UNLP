from flask_wtf import FlaskForm
from wtforms import FileField, HiddenField, SubmitField
from wtforms.validators import DataRequired,  Regexp
from flask_wtf.file import FileField, FileRequired, FileAllowed

class UploadDocumentoForm(FlaskForm):
    legajo_id = HiddenField(validators=[DataRequired()])
    tipo = HiddenField(default="orden_facturacion", validators=[DataRequired()])
    file = FileField(
        "Archivo PDF",
        validators=[
            FileRequired(message="Debe seleccionar un archivo"),
            Regexp(r'^[^/\\]+\.(pdf)$', message="Solo se permiten archivos PDF"),
        ],
    )
    submit = SubmitField("Subir")
    
class DownloadForm(FlaskForm):
    documento_id = HiddenField("ID del documento")
    submit = SubmitField("Descargar")