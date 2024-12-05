from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, IntegerField, ValidationError, MultipleFileField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
import re
from administracion.src.core.servicios import personal as servicio_personal

class FormularioNuevoBien(FlaskForm):
    def validar_solo_numeros(self, field):
        if not re.match(r"^\d+$", field.data):
            raise ValidationError("solo puede contener números.")
        
    titulo = StringField('Titulo', validators=[DataRequired(message="es requerido"), 
                                             Length(max=50,message="no puede exceder los 50 caracteres")],
                       render_kw={"aria-label": "Titulo"}
                       )
    numero_inventario = StringField('Numero de inventario', validators=[DataRequired(message="es requerido"), 
                                                  Length(max=30,message="no puede exceder los 50 caracteres"), 
                                                  validar_solo_numeros],
                                                  render_kw={"aria-label": "Numero de inventario"}
                                                  )
    anio = IntegerField('Año', validators=[DataRequired(message="es requerido"), 
                                           NumberRange(min=1, max=2500, message="debe estar entre 1 y 2500")],
                                         render_kw={"aria-label": "Año"})
    institucion = StringField('Institución', validators=[DataRequired(message="es requerido"), 
                                             Length(max=50,message="no puede exceder los 50 caracteres")],
                       render_kw={"aria-label": "Institución"}
                       )
    descripcion = TextAreaField('Descripción', validators=[DataRequired(message="es requerido"), 
                                             Length(max=200,message="no puede exceder los 200 caracteres")],
                       render_kw={"aria-label": "Descripción"}
                       )
    
    archivos_adjuntos = MultipleFileField('Archivos adjuntos', validators=[Optional()], 
                                          render_kw={"aria-label": "Archivos adjuntos"})

    area = SelectField('Area',coerce=int, validators=[Optional()], render_kw={"aria-label": "Area"})
    
    def __init__(self, *args, **kwargs):
        super(FormularioNuevoBien, self).__init__(*args, **kwargs)
        self.area.choices = [(area.id, f"{area.nombre}") for area in servicio_personal.listar_areas()]