from flask import flash, redirect, render_template, request, url_for, Blueprint, session
from models.personal.ausencia import Ausencia
from models.personal.personal import User
from models.personal.empleado import Empleado

from datetime import datetime, timedelta
from administracion.src.web.controllers.roles import role_required  # Importa el decorador

ausencia_bp = Blueprint("ausencia", __name__, url_prefix="/ausencia")

@ausencia_bp.route('/registrar', methods=['GET', 'POST'])
@role_required('Administrador', 'Colaborador')
def registrar_ausencia():
    if request.method == 'POST':
        empleado_id = request.form['empleado_id']
        fecha_desde = request.form['fecha_desde']
        fecha_hasta = request.form['fecha_hasta']
        motivo = request.form['motivo']
        
        # Crear nueva ausencia
        nueva_ausencia = Ausencia(
            empleado_id=empleado_id,
            fecha_desde=datetime.strptime(fecha_desde, '%Y-%m-%d'),
            fecha_hasta=datetime.strptime(fecha_hasta, '%Y-%m-%d'),
            motivo=motivo
        )
        nueva_ausencia.save()
        flash('Ausencia registrada con éxito', 'success')
        return redirect(url_for('ausencia.registrar_ausencia'))
    
    empleados = Empleado.query.all()
    return render_template('personal/registrar_ausencia.html', empleados=empleados)

@ausencia_bp.route('/calendario', methods=['GET'])
@role_required('Administrador', 'Colaborador')
def ver_calendario():
    # Obtener el mes y año actuales
    hoy = datetime.today()
    mes = request.args.get('mes', hoy.month, type=int)
    año = request.args.get('año', hoy.year, type=int)
    
    # Calcular el primer y último día del mes
    primer_dia = datetime(año, mes, 1)
    if mes == 12:
        ultimo_dia = datetime(año + 1, 1, 1) - timedelta(days=1)
    else:
        ultimo_dia = datetime(año, mes + 1, 1) - timedelta(days=1)
    
    # Obtener la fecha actual
    fecha_actual = hoy.date()
    
    # Obtener las ausencias del mes, ordenadas por fecha de inicio y cuya fecha_hasta no haya pasado de la fecha actual
    ausencias = Ausencia.query.filter(
        Ausencia.fecha_desde <= ultimo_dia,
        Ausencia.fecha_hasta >= primer_dia,
        Ausencia.fecha_hasta >= fecha_actual
    ).order_by(Ausencia.fecha_desde).all()
    
    return render_template('personal/ver_calendario.html', ausencias=ausencias, mes=mes, año=año)