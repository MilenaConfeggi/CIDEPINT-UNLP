from flask_wtf import FlaskForm
from wtforms import FileField
from flask_wtf.file import FileAllowed

class MailForm(FlaskForm):
    archivo = FileField('Archivo', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Solo JPG, PNG y JPEG!')
    ])