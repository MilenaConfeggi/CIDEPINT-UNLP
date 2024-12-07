from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, SelectMultipleField, StringField, FloatField, FieldList, FormField, ValidationError
from wtforms.validators import DataRequired
from models.compras.compra import estado_compra
from models.personal.empleado import Empleado
from models.personal.area import Area
from models.Fondo.fondo import Fondo
from models.compras.proveedor import Proveedor
import re

class DynamicFieldForm(FlaskForm):
    id = StringField('id')
    detalle = StringField('detalle')

class form_agregar_compra(FlaskForm):

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
    observaciones = StringField('observaciones', validators=[DataRequired(
        message="Este campo es requerido")])
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
    fondos = SelectMultipleField('fondos')
    empleados = SelectMultipleField('empleados')
    areas = SelectMultipleField('areas')
    fondos_detalle = FieldList(FormField(DynamicFieldForm))
    empleados_detalle = FieldList(FormField(DynamicFieldForm))
    areas_detalle = FieldList(FormField(DynamicFieldForm))
    
    def __init__(self, *args, **kwargs):
        super(form_agregar_compra, self).__init__(*args, **kwargs)

        fondos_choices = [(fondo.titulo, fondo.titulo) for fondo in Fondo.query.all()]
        empleados_choices = [(empleado.id, f"{empleado.nombre} {empleado.apellido}") 
                             for empleado in Empleado.query.all() if empleado.habilitado]
        areas_choices = [(area.id, area.nombre) for area in Area.query.all()]
        proveedores_choices = [(proveedor.id, proveedor.razon_social) for proveedor in Proveedor.query.all() if proveedor.activo]

        self.fondos.choices = fondos_choices 
        self.empleados.choices = empleados_choices
        self.areas.choices = areas_choices
        self.proveedor.choices = proveedores_choices
        self.solicitante.choices = empleados_choices