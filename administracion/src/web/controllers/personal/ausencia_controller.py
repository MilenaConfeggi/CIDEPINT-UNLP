from flask import flash, redirect, render_template, request, url_for, Blueprint, session
from models.personal.ausencia import Ausencia
from models.personal.personal import User
from models.personal.empleado import Empleado
from administracion.src.core.servicios import personal as servicio_personal
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
            empleado=servicio_personal.conseguir_empleado_de_id(empleado_id),
            fecha_desde=datetime.strptime(fecha_desde, '%Y-%m-%d'),
            fecha_hasta=datetime.strptime(fecha_hasta, '%Y-%m-%d'),
            motivo=motivo
        )
        nueva_ausencia.save()
        flash('Ausencia registrada con éxito', 'success')
        return redirect(url_for('ausencia.ver_calendario'))
    
    empleados = Empleado.query.all()
    return render_template('personal/registrar_ausencia.html', empleados=empleados)

@ausencia_bp.route('/calendario', methods=['GET'])
@role_required('Administrador', 'Colaborador')
def ver_calendario():
    # Obtener el mes y año actuales
    hoy = datetime.today()
    mes = request.args.get('mes', hoy.month, type=int)
    anio = request.args.get('anio', hoy.year, type=int)
    
    # Calcular el primer y último día del mes
    primer_dia = datetime(anio, mes, 1)

    # Calcula el primer día de la semana
    dia_empezar = primer_dia - timedelta(days=primer_dia.weekday())

    # Calcula el último día del mes
    mes_siguiente = (primer_dia.replace(day=28) + timedelta(days=4)).replace(day=1)
    ultimo_dia = mes_siguiente - timedelta(days=1)

    # Genera todos los días del mes
    dias = []
    dia_actual = dia_empezar
    while dia_actual <= ultimo_dia:
        dias.append(dia_actual)
        dia_actual += timedelta(days=1)
    
    # Obtener las ausencias del mes, ordenadas por fecha de inicio
    ausencias = Ausencia.query.filter(
        Ausencia.fecha_desde <= ultimo_dia,
        Ausencia.fecha_hasta >= primer_dia,
    ).order_by(Ausencia.fecha_desde).all()
    
    return render_template('personal/ver_calendario.html', ausencias=ausencias, dias=dias, primer_dia=primer_dia, ultimo_dia=ultimo_dia, mes=mes, anio=anio)

@ausencia_bp.post('/eliminar')
@role_required('Administrador', 'Colaborador')
def eliminar_ausencia():
    id_ausencia = request.form['id_ausencia']
    
    if servicio_personal.eliminar_ausencia(id_ausencia=id_ausencia):
        flash('Ausencia eliminada correctamente', 'success')
    else:
        flash('Error al eliminar la ausencia', 'error')
    return redirect(url_for('ausencia.ver_calendario'))