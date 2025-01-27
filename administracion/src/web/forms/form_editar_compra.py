from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, FloatField, FieldList, FormField, ValidationError
from wtforms.validators import DataRequired
from models.compras.compra import estado_compra
from administracion.src.core.servicios.personal import listar_empleados, listar_areas
from administracion.src.core.fondos.fondo import listar_fondos_activos 
from administracion.src.core.proveedores.proveedor import listar_proveedores
import re

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
        self.id_fondo.choices = [(fondo.id, fondo.titulo) for fondo in listar_fondos_activos()]


class form_editar_compra(FlaskForm):

    def validar_solo_numeros(self, field):
        if not re.match(r"^-?\d*(\.\d+)?$", str(field.data)):
            raise ValidationError("El campo debe ser un número válido.")

    fecha = DateField('fecha', validators=[DataRequired(
        message="Este campo es requerido")])
    descripcion = StringField('descripcion', validators=[DataRequired(
        message="Este campo es requerido")])
    proveedor = SelectField('proveedor', validators=[DataRequired(
        message="Este campo es requerido")])
    solicitante = SelectField('solicitante', validators=[DataRequired(
        message="Este campo es requerido")])
    importe = FloatField('importe', validators=[DataRequired(
        message="Este campo es requerido"), validar_solo_numeros])
    observaciones = StringField('observaciones')
    estado = SelectField('estado', 
        choices=[
            (estado.name, estado.value)
            for estado in reversed(estado_compra)
            if estado.name != "CANCELADA" 
        ],                 
        validators=[DataRequired(
        message="Este campo es requerido")])
    numero_factura = StringField('numero_factura', validators=[DataRequired(
        message="Este campo es requerido")])
    fondos = FieldList(FormField(FormularioFondo), min_entries=0)
    empleados = FieldList(FormField(FormularioEmpleado), min_entries=0)
    areas = FieldList(FormField(FormularioArea), min_entries=0)
    
    def __init__(self, *args, **kwargs):
        super(form_editar_compra, self).__init__(*args, **kwargs)

        empleados_choices = [(empleado.id, f"{empleado.nombre} {empleado.apellido} - {empleado.dni}") 
                             for empleado in listar_empleados()]
        proveedores_choices = [(proveedor.id, proveedor.razon_social) for proveedor in listar_proveedores()]

        self.proveedor.choices = proveedores_choices
        self.solicitante.choices = empleados_choices