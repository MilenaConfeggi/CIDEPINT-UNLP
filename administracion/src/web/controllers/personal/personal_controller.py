from flask import flash, redirect, render_template, request, send_file, url_for, Blueprint, session
from models.personal.personal import User
from models.personal.area import Area
from models.personal.archivo import Archivo
from io import BytesIO
from werkzeug.utils import secure_filename
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import send_file
from sqlalchemy import or_, cast
from sqlalchemy.types import String
import pandas as pd
from administracion.src.web.controllers.roles import role_required
from flask_login import current_user

personal_bp = Blueprint("personal", __name__, url_prefix="/personal")

@personal_bp.route('/', methods=['GET'])
@role_required('Administrador', 'Colaborador', 'Personal')
def index():
    areas = Area.query.all()
    return render_template('personal/index.html', areas=areas)

@personal_bp.route('/registrar', methods=['GET', 'POST'])
@role_required('Administrador', 'Colaborador')  
def registrar_usuario():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        area_id = request.form['area_id']
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        dependencia = request.form['dependencia']
        cargo = request.form['cargo']
        subdivision_cargo = request.form['subdivision_cargo']
        telefono = request.form.get('telefono')
        domicilio = request.form.get('domicilio')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        observaciones = request.form.get('observaciones')
        rol = request.form['rol']
        
        # Verificar si el usuario ya existe
        existing_user = User.query.filter(or_(User.username == username, User.email == email)).first()
        if existing_user:
            flash('El usuario, correo electrónico o DNI ya existe', 'error')
            return redirect(url_for('personal.registrar_usuario'))
        
        # Crear nuevo usuario
        nuevo_usuario = User(
            username=username,
            password=password
        )
        success, message = nuevo_usuario.save()
        if success:
            # Crear empleado asociado al usuario
            nuevo_empleado = Empleado(
                user_id=nuevo_usuario.id,
                email=email,
                area_id=area_id,
                dni=dni,
                nombre=nombre,
                apellido=apellido,
                dependencia=dependencia,
                cargo=cargo,
                subdivision_cargo=subdivision_cargo,
                telefono=telefono,
                domicilio=domicilio,
                fecha_nacimiento=fecha_nacimiento,
                observaciones=observaciones,
                rol=rol
            )
            success, message = nuevo_empleado.save()
            if success:
                flash('Usuario registrado con éxito', 'success')
            else:
                flash(message, 'error')
        else:
            flash(message, 'error')
        return redirect(url_for('personal.registrar_usuario'))
    
    # Recuperar las áreas de la base de datos
    areas = Area.query.all()
    
    # Determinar las opciones de rol disponibles según el rol del usuario actual
    if current_user.empleado.rol == 'Administrador':
        roles_disponibles = ['Colaborador', 'Administrador', 'Personal']
    elif current_user.empleado.rol == 'Colaborador':
        roles_disponibles = ['Personal']
    else:
        roles_disponibles = []

    campos = [
        {'name': 'username', 'label': 'Nombre de Usuario', 'type': 'text', 'required': True},
        {'name': 'password', 'label': 'Contraseña', 'type': 'password', 'required': True},
        {'name': 'email', 'label': 'Correo Electrónico', 'type': 'email', 'required': True},
        {'name': 'area_id', 'label': 'Área', 'type': 'select', 'required': True, 'options': [(area.id, area.nombre) for area in areas]},
        {'name': 'dni', 'label': 'DNI', 'type': 'text', 'required': True},
        {'name': 'nombre', 'label': 'Nombre', 'type': 'text', 'required': True},
        {'name': 'apellido', 'label': 'Apellido', 'type': 'text', 'required': True},
        {'name': 'dependencia', 'label': 'Dependencia', 'type': 'select', 'required': True, 'options': ['UNLP', 'CIC', 'CONICET']},
        {'name': 'cargo', 'label': 'Cargo', 'type': 'select', 'required': True, 'options': ['Investigador', 'CPA', 'Administrativo', 'Técnico']},
        {'name': 'subdivision_cargo', 'label': 'Subdivisión del Cargo', 'type': 'select', 'required': True, 'options': {
            'Investigador': ['Asistente', 'Adjunto', 'Independiente', 'Principal', 'Superior'],
            'CPA': ['Profesional Principal', 'Profesional Adjunto', 'Profesional Asistente'],
            'Técnico': ['Profesional', 'Asociado', 'Asistente', 'Auxiliar'],
            'Administrativo': ['ART 9', 'Ley 10430']
        }},
        {'name': 'telefono', 'label': 'Teléfono', 'type': 'text', 'required': False},
        {'name': 'domicilio', 'label': 'Domicilio', 'type': 'text', 'required': False},
        {'name': 'fecha_nacimiento', 'label': 'Fecha de Nacimiento', 'type': 'date', 'required': False},
        {'name': 'observaciones', 'label': 'Observaciones', 'type': 'textarea', 'required': False},
        {'name': 'rol', 'label': 'Rol', 'type': 'select', 'required': True, 'options': roles_disponibles}
    ]
    
    return render_template('personal/registrar_usuario.html', campos=campos)

@personal_bp.route('/empleados', methods=['GET'])
@role_required('Administrador', 'Colaborador')
def ver_empleados():
    busqueda = request.args.get('busqueda', None)
    ordenar_por = request.args.get('ordenar_por', 'nombre')
    orden = request.args.get('orden', 'asc')
    mostrar_inhabilitados = request.args.get('mostrar_inhabilitados', '0') == '1'
    
    query = Empleado.query
    
    if busqueda:
        query = query.filter(or_(
            Empleado.nombre.ilike(f'%{busqueda}%'),
            Empleado.apellido.ilike(f'%{busqueda}%'),
            cast(Empleado.dni, String).ilike(f'%{busqueda}%'),
            cast(Empleado.area, String).ilike(f'%{busqueda}%'),
            cast(Empleado.dependencia, String).ilike(f'%{busqueda}%'),
            cast(Empleado.cargo, String).ilike(f'%{busqueda}%')
        ))
    
    if not mostrar_inhabilitados:
        query = query.filter_by(habilitado=True)
    
    if orden == 'asc':
        query = query.order_by(cast(getattr(Empleado, ordenar_por), String).asc())
    else:
        query = query.order_by(cast(getattr(Empleado, ordenar_por), String).desc())
    
    empleados = query.all()
    
    return render_template('personal/ver_empleados.html', empleados=empleados, busqueda=busqueda, ordenar_por=ordenar_por, orden=orden, mostrar_inhabilitados=mostrar_inhabilitados)

@personal_bp.route('/empleados/descargar', methods=['GET'])
@role_required('Administrador', 'Colaborador')  
def descargar_empleados():
    formato = request.args.get('formato', 'excel')
    busqueda = request.args.get('busqueda', None)
    ordenar_por = request.args.get('ordenar_por', 'nombre')
    orden = request.args.get('orden', 'asc')
    
    query = Empleado.query.filter_by(habilitado=True)
    
    if busqueda:
        query = query.filter(or_(
            Empleado.nombre.ilike(f'%{busqueda}%'),
            Empleado.apellido.ilike(f'%{busqueda}%'),
            cast(Empleado.dni, String).ilike(f'%{busqueda}%'),
            cast(Empleado.area, String).ilike(f'%{busqueda}%'),
            cast(Empleado.dependencia, String).ilike(f'%{busqueda}%'),
            cast(Empleado.cargo, String).ilike(f'%{busqueda}%')
        ))
    
    if orden == 'asc':
        query = query.order_by(cast(getattr(Empleado, ordenar_por), String).asc())
    else:
        query = query.order_by(cast(getattr(Empleado, ordenar_por), String).desc())
    
    empleados = query.all()
    
    if formato == 'pdf':
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        y = height - 40
        for empleado in empleados:
            c.drawString(30, y, f"Nombre: {empleado.nombre} {empleado.apellido}, DNI: {empleado.dni}, Dependencia: {empleado.dependencia}, Área: {empleado.area}, Cargo: {empleado.cargo}")
            y -= 20
            if y < 40:
                c.showPage()
                y = height - 40
        
        c.save()
        buffer.seek(0)
        return send_file(buffer, download_name='empleados.pdf', as_attachment=True)
    
    elif formato == 'excel':
        data = [{
            'Nombre': empleado.nombre,
            'Apellido': empleado.apellido,
            'DNI': empleado.dni,
            'Dependencia': empleado.dependencia,
            'Área': empleado.area,
            'Cargo': empleado.cargo
        } for empleado in empleados]
        
        df = pd.DataFrame(data)
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Empleados')
        
        buffer.seek(0)
        return send_file(buffer, download_name='empleados.xlsx', as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
    return redirect(url_for('personal.ver_empleados'))

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@personal_bp.route('/perfil/<int:id>', methods=['GET', 'POST'])
@role_required('Administrador', 'Colaborador', 'Personal') 
def ver_perfil(id):
    user = User.query.get_or_404(id)
    
    # Verificar si el usuario actual tiene permiso para ver este perfil
    if current_user.empleado.rol == 'Personal' and current_user.id != user.id:
        flash('No tienes permiso para ver este perfil.', 'error')
        return redirect(url_for('personal.ver_perfil', id=current_user.id))
    
    if request.method == 'POST':
        if 'archivo' in request.files:
            archivo = request.files['archivo']
            tipo = request.form.get('tipo')
            if not tipo:
                flash('Debe indicar el tipo de archivo', 'error')
                return redirect(url_for('personal.ver_perfil', id=user.id))
            if archivo and allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                ruta = os.path.join(UPLOAD_FOLDER, filename)
                archivo.save(ruta)
                
                nuevo_archivo = Archivo(
                    empleado_id=user.empleado.id,
                    nombre=filename,
                    tipo=tipo,
                    ruta=ruta
                )
                nuevo_archivo.save()
                flash('Archivo subido con éxito', 'success')
                return redirect(url_for('personal.ver_perfil', id=user.id))
        
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.empleado.nombre = request.form.get('nombre')
        user.empleado.apellido = request.form.get('apellido')
        user.empleado.dni = request.form.get('dni')
        user.empleado.dependencia = request.form.get('dependencia')
        user.empleado.cargo = request.form.get('cargo')
        user.empleado.fecha_nacimiento = request.form.get('fecha_nacimiento')
        user.empleado.telefono = request.form.get('telefono')
        user.empleado.domicilio = request.form.get('domicilio')
        user.empleado.observaciones = request.form.get('observaciones')
        
        # Solo permitir modificar el área si el usuario no es 'Personal'
        if current_user.empleado.rol != 'Personal':
            user.empleado.area_id = request.form.get('area_id')
        
        if request.form.get('password'):
            user.set_password(request.form.get('password'))
        
        success, message = user.update()
        if success:
            flash('Perfil actualizado con éxito', 'success')
        else:
            flash(message, 'error')
        return redirect(url_for('personal.ver_perfil', id=user.id))
    
    area = Area.query.filter_by(id=user.empleado.area_id).first()
    saldo_area = area.saldo if area else 'N/A'
    archivos = Archivo.query.filter_by(empleado_id=user.empleado.id).all()
    
    # Obtener la lista de áreas y otros valores necesarios para los select options
    areas = Area.query.all()
    dependencias = ['UNLP', 'CIC', 'CONICET']
    cargos = ['Investigador', 'CPA', 'Administrativo', 'Técnico']
    subdivisiones_cargo = {
        'Investigador': ['Asistente', 'Adjunto', 'Independiente', 'Principal', 'Superior'],
        'CPA': ['Profesional Principal', 'Profesional Adjunto', 'Profesional Asistente'],
        'Técnico': ['Profesional', 'Asociado', 'Asistente', 'Auxiliar'],
        'Administrativo': ['ART 9', 'Ley 10430']
    }
    
    campos = [
        {'name': 'username', 'label': 'Nombre de Usuario', 'type': 'text', 'value': user.username},
        {'name': 'email', 'label': 'Correo Electrónico', 'type': 'email', 'value': user.empleado.email},
        {'name': 'nombre', 'label': 'Nombre', 'type': 'text', 'value': user.empleado.nombre},
        {'name': 'apellido', 'label': 'Apellido', 'type': 'text', 'value': user.empleado.apellido},
        {'name': 'dni', 'label': 'DNI', 'type': 'text', 'value': user.empleado.dni},
        {'name': 'area_id', 'label': 'Área', 'type': 'select', 'value': user.empleado.area_id, 'options': [(area.id, area.nombre) for area in areas], 'disabled': current_user.empleado.rol == 'Personal'},
        {'name': 'dependencia', 'label': 'Dependencia', 'type': 'select', 'value': user.empleado.dependencia, 'options': dependencias},
        {'name': 'cargo', 'label': 'Cargo', 'type': 'select', 'value': user.empleado.cargo, 'options': cargos},
        {'name': 'subdivision_cargo', 'label': 'Subdivisión del Cargo', 'type': 'select', 'value': user.empleado.subdivision_cargo, 'options': subdivisiones_cargo.get(user.empleado.cargo, [])},
        {'name': 'fecha_nacimiento', 'label': 'Fecha de Nacimiento', 'type': 'date', 'value': user.empleado.fecha_nacimiento},
        {'name': 'telefono', 'label': 'Teléfono', 'type': 'text', 'value': user.empleado.telefono},
        {'name': 'domicilio', 'label': 'Domicilio', 'type': 'text', 'value': user.empleado.domicilio},
        {'name': 'observaciones', 'label': 'Observaciones', 'type': 'textarea', 'value': user.empleado.observaciones},
    ]
    
    return render_template('personal/ver_perfil.html', user=user, saldo_area=saldo_area, archivos=archivos, campos=campos)

@personal_bp.route('/archivo/eliminar/<int:id>', methods=['POST'])
@role_required('Administrador', 'Colaborador', 'Personal') 
def eliminar_archivo(id):
    archivo = Archivo.query.get_or_404(id)
    archivo.delete()
    os.remove(archivo.ruta)
    flash('Archivo eliminado con éxito', 'success')
    return redirect(url_for('personal.ver_perfil', id=archivo.empleado_id))

@personal_bp.route('/archivo/descargar/<int:id>', methods=['GET'])
@role_required('Administrador', 'Colaborador', 'Personal') 
def descargar_archivo(id):
    archivo = Archivo.query.get_or_404(id)    
    return send_file(archivo.ruta, as_attachment=True)

@personal_bp.route('/usuario/inhabilitar/<int:id>', methods=['POST'])
@role_required('Administrador', 'Colaborador') 
def inhabilitar_usuario(id):
    user = User.query.get_or_404(id)
    current_user = User.query.get(session['user_id'])  # Asumiendo que el ID del usuario actual está en la sesión
    
    # Verificar permisos
    if current_user.empleado.cargo not in ['Colaborador', 'Administrador']:
        flash('No tienes permiso para inhabilitar este usuario', 'error')
        return redirect(url_for('personal.ver_perfil', id=user.id))
    
    user.empleado.habilitado = False
    user.update()
    flash('Usuario inhabilitado con éxito', 'success')
    return redirect(url_for('personal.ver_perfil', id=user.id))

@personal_bp.route('/topicos', methods=['GET'])
@role_required('Administrador', 'Colaborador', 'Personal') 
def seleccionar_topico():
    return render_template('topicos.html')