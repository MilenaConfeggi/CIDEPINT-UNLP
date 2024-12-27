from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, FieldList, FormField
from wtforms.validators import DataRequired
from administracion.src.core.servicios.personal import listar_empleados, listar_areas
from administracion.src.core.fondos.fondo import listar_fondos 
class FormularioEmpleado(FlaskForm):
    id_empleado = SelectField('Empleado', choices=[], coerce=int, validators=[DataRequired()])
    monto = FloatField('Monto', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(FormularioEmpleado, self).__init__(*args, **kwargs)
        self.id_empleado.choices = [(empleado.id, f"{empleado.nombre} {empleado.apellido} - {empleado .dni}") for empleado in listar_empleados()]

class FormularioArea(FlaskForm):
    id_area = SelectField('Area', choices=[], coerce=int, validators=[DataRequired()])
    monto = FloatField('Monto', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(FormularioArea, self).__init__(*args, **kwargs)
        self.id_area.choices = [(area.id, area.nombre) for area in listar_areas()]

class FormularioFondo(FlaskForm):
    id_fondo = SelectField('Fondo', choices=[], coerce=str, validators=[DataRequired()])
    monto = FloatField('Monto', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(FormularioFondo, self).__init__(*args, **kwargs)
        self.id_fondo.choices = [(fondo.id, fondo.titulo) for fondo in listar_fondos()]


class form_aprobar_compra(FlaskForm):

    fondos = FieldList(FormField(FormularioFondo), min_entries=0)
    empleados = FieldList(FormField(FormularioEmpleado), min_entries=0)
    areas = FieldList(FormField(FormularioArea), min_entries=0)