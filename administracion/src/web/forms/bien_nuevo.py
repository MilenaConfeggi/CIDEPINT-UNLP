from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Length, Optional, NumberRange
import re

class FormularioNuevoBien(FlaskForm):
    def validar_solo_numeros(self, field):
        if not re.match(r"^\d+$", field.data):
            raise ValidationError("El campo solo puede contener números.")
        
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
                                           NumberRange(min=1900, max=2500, message="debe estar entre 1900 y 2500")],
                                         render_kw={"aria-label": "Año"})
    institucion = StringField('Institución', validators=[DataRequired(message="es requerido"), 
                                             Length(max=50,message="no puede exceder los 50 caracteres")],
                       render_kw={"aria-label": "Institución"}
                       )
    descripcion = TextAreaField('Descripción', validators=[DataRequired(message="es requerido"), 
                                             Length(max=200,message="no puede exceder los 200 caracteres")],
                       render_kw={"aria-label": "Descripción"}
                       )
    
    area = SelectField('Area',coerce=int, validators=[Optional()], render_kw={"aria-label": "Area"})
    
    def __init__(self, *args, **kwargs):
        super(FormularioNuevoBien, self).__init__(*args, **kwargs)
        self.area.choices = [(area['id'], f"{area['nombre']}") for area in [{'id': 1, 'nombre' : 'Servicios'}]]
        #self.area.choices = [(area.id, f"{area.nombre}") for area in servicio_area.listar_areas()]