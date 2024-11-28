from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length, NumberRange, Optional
import re


class FormularioNuevaDistribucion(FlaskForm):
    def validar_solo_numeros(self, field):
        if not re.match(r"^\d+$", field.data):
            raise ValidationError("El campo solo puede contener números.")

    porcentaje_area = FloatField('Porcentaje Area', 
                                 validators=[
                                     DataRequired(message="es requerido"),
                                     NumberRange(min=0, max=100, message="Debe estar entre 0 y 100")
                                 ],
                                 render_kw={"aria-label": "Porcentaje Area"}
                                 )
    
    porcentaje_empleados = FloatField('Porcentaje Empleados', 
                                      validators=[
                                          DataRequired(message="es requerido"),
                                          NumberRange(min=0, max=100, message="Debe estar entre 0 y 100")
                                      ],
                                      render_kw={"aria-label": "Porcentaje Empleados"}
                                      )
    
    porcentaje_comisiones = FloatField('Porcentaje Comisiones', 
                                       validators=[
                                           DataRequired(message="es requerido"),
                                           NumberRange(min=0, max=100, message="Debe estar entre 0 y 100")
                                       ],
                                       render_kw={"aria-label": "Porcentaje Comisiones"}
                                       )
    
    monto_a_distribuir = FloatField('Monto a Distribuir', 
                                    validators=[
                                        DataRequired(message="es requerido"),
                                        NumberRange(min=0, message="Debe ser un valor positivo")
                                    ],
                                    render_kw={"aria-label": "Monto a Distribuir"}
                                    )
    
    costos = FloatField('Costos', 
                        validators=[
                            DataRequired(message="es requerido"),
                            NumberRange(min=0, message="Debe ser un valor positivo")
                        ],
                        render_kw={"aria-label": "Costos"}
                        )
    
    legajo_id = IntegerField('Legajo ID', 
                             validators=[
                                 DataRequired(message="es requerido"),
                                 NumberRange(min=1, message="Debe ser un ID válido")
                             ],
                             render_kw={"aria-label": "Legajo ID"}
                             )
    
    ganancias_de_id = SelectField('Area de Ganancias', 
                                  coerce=int, 
                                  validators=[Optional()], 
                                  render_kw={"aria-label": "Area de Ganancias"})
    
    costos_de_id = SelectField('Area de Costos', 
                               coerce=int, 
                               validators=[Optional()], 
                               render_kw={"aria-label": "Area de Costos"})
    
    def __init__(self, *args, **kwargs):
        super(FormularioNuevaDistribucion, self).__init__(*args, **kwargs)
        # Poblamos las opciones de los SelectField con datos simulados (esto debería conectarse a la base de datos)
        #self.ganancias_de_id.choices = [(area['id'], f"{area['nombre']}") for area in [{'id': 1, 'nombre': 'Ventas'}, {'id': 2, 'nombre': 'Producción'}]]
        #self.costos_de_id.choices = [(area['id'], f"{area['nombre']}") for area in [{'id': 3, 'nombre': 'Logística'}, {'id': 4, 'nombre': 'Compras'}]]
