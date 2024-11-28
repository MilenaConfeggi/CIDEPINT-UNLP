from flask import flash, redirect, render_template, request, url_for, Blueprint, session
from src.core.models.ausencia import Ausencia
from src.core.models.personal import User
from datetime import datetime, timedelta

ausencia_bp = Blueprint("ausencia", __name__, url_prefix="/ausencia")

@ausencia_bp.route('/registrar', methods=['GET', 'POST'])
def registrar_ausencia():
    if request.method == 'POST':
        empleado_id = request.form['empleado_id']
        fecha_desde = request.form['fecha_desde']
        fecha_hasta = request.form['fecha_hasta']
        motivo = request.form['motivo']
        
        # Verificar permisos
        current_user = User.query.get(session['user_id'])
        if current_user.cargo not in ['Colaborador', 'Administrador']:
            flash('No tienes permiso para registrar ausencias', 'error')
            return redirect(url_for('ausencia.registrar_ausencia'))
        
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
    
    empleados = User.query.all()
    return render_template('ausencia/registrar_ausencia.html', empleados=empleados)

@ausencia_bp.route('/calendario', methods=['GET'])
def ver_calendario():
    # Verificar permisos
    current_user = User.query.get(session['user_id'])
    if current_user.cargo not in ['Colaborador', 'Administrador']:
        flash('No tienes permiso para ver el calendario de ausencias', 'error')
        return redirect(url_for('personal.ver_empleados'))
    
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
    
    # Obtener las ausencias del mes
    ausencias = Ausencia.query.filter(Ausencia.fecha_desde <= ultimo_dia, Ausencia.fecha_hasta >= primer_dia).all()
    
    # Crear un diccionario para almacenar las ausencias por día
    calendario = {}
    for i in range((ultimo_dia - primer_dia).days + 1):
        dia = primer_dia + timedelta(days=i)
        calendario[dia] = []
    
    # Llenar el diccionario con las ausencias
    for ausencia in ausencias:
        for i in range((ausencia.fecha_hasta - ausencia.fecha_desde).days + 1):
            dia = ausencia.fecha_desde + timedelta(days=i)
            if dia in calendario:
                calendario[dia].append(ausencia)
    
    return render_template('ausencia/ver_calendario.html', calendario=calendario, mes=mes, año=año)