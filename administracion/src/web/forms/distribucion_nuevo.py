from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, ValidationError, SelectMultipleField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
import re
from administracion.src.core import Area as areaDB
from administracion.src.core import Empleado as empleadoDB
class FormularioNuevaDistribucion(FlaskForm):
    def validar_solo_numeros(self, field):
        if not re.match(r"^\d+$", field.data):
            raise ValidationError("El campo solo puede contener números.")

    porcentaje_area = FloatField('Porcentaje Area', 
                                 validators=[
                                     DataRequired(message="no puede ser 0"),
                                     NumberRange(min=0, max=100, message="Debe estar entre 0 y 100")
                                 ],
                                 render_kw={"aria-label": "Porcentaje Area"}
                                 )
    
    porcentaje_empleados = FloatField('Porcentaje Empleados', 
                                      validators=[
                                          NumberRange(min=0, max=100, message="Debe estar entre 0 y 100")
                                      ],
                                      render_kw={"aria-label": "Porcentaje Empleados"}
                                      )
    
    porcentaje_comisiones = FloatField('Porcentaje Comisiones', 
                                       validators=[
                                           
                                           NumberRange(min=0, max=100, message="Debe estar entre 0 y 100")
                                       ],
                                       render_kw={"aria-label": "Porcentaje Comisiones"}
                                       )
    
    monto_a_distribuir = FloatField('Monto a Distribuir', 
                                    validators=[
                                        DataRequired(message="no puede ser 0"),
                                        NumberRange(min=0, message="Debe ser un valor positivo")
                                    ],
                                    render_kw={"aria-label": "Monto a Distribuir"}
                                    )
    
    costos = FloatField('Costos', 
                        validators=[
                        
                            NumberRange(min=0, message="Debe ser un valor positivo"),
                            Optional()
                        ],
                        render_kw={"aria-label": "Costos"}
                        )
    
    ganancias_de_id = SelectField('Area de Ganancias', coerce=int, validators=[DataRequired(message="es requerido")], render_kw={"aria-label": "Area de Ganancias"})
    
    costos_de_id = SelectField('Area de Costos', coerce=int, validators=[DataRequired(message="es requerido")], render_kw={"aria-label": "Area de Costos"})
    
    # Seleccionar Empleados
    
    empleados_seleccionados = SelectMultipleField(
        'Seleccionar Empleados',
        coerce=int,
        validators=[Optional()],
        render_kw={"aria-label": "Seleccionar Empleados"}
    )

    def __init__(self, *args, **kwargs):
        super(FormularioNuevaDistribucion, self).__init__(*args, **kwargs)
        # Poblamos las opciones de los SelectField con datos simulados (esto debería conectarse a la base de datos)
        self.ganancias_de_id.choices = [(area.id, f"{area.nombre}") for area in areaDB.list_areas()]
        self.costos_de_id.choices = [(area.id, f"{area.nombre}") for area in areaDB.list_areas()]
        self.empleados_seleccionados.choices = sorted(
            [(empleado.id, f"{empleado.nombre} {empleado.apellido} ({empleado.dni})") for empleado in empleadoDB.list_empleados() if empleado.user.habilitado],
            key=lambda x: x[1]
        )