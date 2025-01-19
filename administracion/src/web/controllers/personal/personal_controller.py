from flask import flash, redirect, render_template, request, send_file, url_for, Blueprint, session, current_app
from flask_mail import Message
from models.personal.personal import User
from models.personal.area import Area
from administracion.src.core.servicios import personal as servicio_personal
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
from models.personal.personal import User
from models.personal.empleado import Empleado
from models.archivos_admin.archivo import Archivo


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
        area = servicio_personal.conseguir_area_de_id(request.form['area_id'])
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        dependencia = request.form.get('dependencia') or None
        cargo = request.form.get('cargo') or None
        subdivision_cargo = request.form.get('subdivision_cargo') or None
        telefono = request.form.get('telefono') or None
        domicilio = request.form.get('domicilio') or None
        fecha_nacimiento = request.form.get('fecha_nacimiento') or None
        observaciones = request.form.get('observaciones') or None
        rol = request.form['rol']
        
        # Verificar si el usuario ya existe
        existing_user = User.query.join(Empleado).filter(
            or_(User.username == username, Empleado.email == email)
        ).first()
        if existing_user:
            flash('El usuario, correo electrónico o DNI ya existe', 'error')
            return redirect(url_for('personal.registrar_usuario'))
        
        # Crear nuevo usuario
        nuevo_usuario = User(
            username=username,
            password=password,
            rol=rol
        )
            # Crear empleado asociado al usuario
        nuevo_empleado = Empleado(
            user=nuevo_usuario,
            email=email,
            area=area,
            dni=dni,
            nombre=nombre,
            apellido=apellido,
            dependencia=dependencia,
            cargo=cargo,
            subdivision_cargo=subdivision_cargo,
            telefono=telefono,
            domicilio=domicilio,
            fecha_nacimiento=fecha_nacimiento,
            observaciones=observaciones
        )
        success, message = nuevo_empleado.save()
        if success:
            msg = Message('Nuevo usuario', sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=[email])
            #Añadir link
            msg.body = f'Se ha creado un nuevo usuario para esta dirección de correo electrónico en la página de administración del CIDEPINT. Tus datos para acceder a la página son Usuario: {username} y Contraseña: {password}'
            mail = current_app.extensions.get('mail')  # Obtén la instancia de Mail desde la aplicación
            mail.send(msg)
            flash('Usuario registrado con éxito', 'success')
        else:
            flash(message, 'error')
        return redirect(url_for('personal.ver_empleados'))
    
    # Recuperar las áreas de la base de datos
    areas = Area.query.all()
    
    # Determinar las opciones de rol disponibles según el rol del usuario actual
    if current_user.rol == 'Administrador':
        roles_disponibles = ['Colaborador', 'Administrador', 'Personal']
    elif current_user.rol == 'Colaborador':
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
        {'name': 'dependencia', 'label': 'Dependencia', 'type': 'select', 'required': False, 'options': ['UNLP', 'CIC', 'CONICET']},
        {'name': 'cargo', 'label': 'Cargo', 'type': 'select', 'required': False, 'options': ['Investigador', 'CPA', 'Administrativo', 'Técnico']},
        {'name': 'subdivision_cargo', 'label': 'Subdivisión del Cargo', 'type': 'select', 'required': False, 'options': {
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
    pagina = request.args.get('pagina', 1, type=int)
    
    query = Empleado.query
    
    if busqueda:
        query = query.filter(or_(
            Empleado.nombre.ilike(f'{busqueda}%'),
            Empleado.apellido.ilike(f'{busqueda}%')
        ))
    
    if not mostrar_inhabilitados:
        query = query.join(User).filter(User.habilitado == True)
    
    if orden == 'asc':
        query = query.order_by(cast(getattr(Empleado, ordenar_por), String).asc())
    else:
        query = query.order_by(cast(getattr(Empleado, ordenar_por), String).desc())

    empleados = query.paginate(page=pagina,per_page=10,error_out=False)
    
    return render_template('personal/ver_empleados.html', empleados=empleados, busqueda=busqueda, ordenar_por=ordenar_por, orden=orden, mostrar_inhabilitados=mostrar_inhabilitados)

@personal_bp.route('/empleados/descargar', methods=['GET'])
@role_required('Administrador', 'Colaborador')  
def descargar_empleados():
    formato = request.args.get('formato', 'excel')
    busqueda = request.args.get('busqueda', None)
    ordenar_por = request.args.get('ordenar_por', 'nombre')
    orden = request.args.get('orden', 'asc')
    mostrar_inhabilitados = request.args.get('mostrar_inhabilitados', False) == 'True'
    
    query = Empleado.query

    print(request.args.get('mostrar_inhabilitados'))
    print(mostrar_inhabilitados)

    if not mostrar_inhabilitados:
        query = query.join(User).filter(User.habilitado == True)
    
    if busqueda:
        query = query.filter(or_(
            Empleado.nombre.ilike(f'{busqueda}%'),
            Empleado.apellido.ilike(f'{busqueda}%'),
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

@personal_bp.route('/perfil/<int:id>', methods=['GET', 'POST'])
@role_required('Administrador', 'Colaborador', 'Personal') 
def ver_perfil(id):
    user = User.query.get_or_404(id)
    
    # Verificar si el usuario actual tiene permiso para ver este perfil
    if current_user.rol == 'Personal' and current_user.id != user.id:
        flash('No tienes permiso para ver este perfil.', 'error')
        return redirect(url_for('personal.ver_perfil', id=current_user.id))
    
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        
        if form_type == 'upload_file':
            if 'archivo' in request.files:
                archivo = request.files['archivo']
                if archivo:
                    servicio_personal.guardar_archivo(user.empleado.id, archivo, tipo=request.form.get('tipo'))
                    flash('Archivo subido con éxito', 'success')
                    return redirect(url_for('personal.ver_perfil', id=user.id))
        
        elif form_type == 'update_profile':
            # Validar campos obligatorios
            username = request.form.get('username')
            email = request.form.get('email')
            nombre = request.form.get('nombre')
            apellido = request.form.get('apellido')
            dni = request.form.get('dni')
            
            if not username or not email or not nombre or not apellido or not dni:
                flash('Todos los campos obligatorios deben ser completados.', 'error')
                return redirect(url_for('personal.ver_perfil', id=user.id))
            
            user.username = username
            user.empleado.email = email
            user.empleado.nombre = nombre
            user.empleado.apellido = apellido
            user.empleado.dni = dni
            user.empleado.dependencia = request.form.get('dependencia')
            user.empleado.cargo = request.form.get('cargo')
            user.empleado.fecha_nacimiento = request.form.get('fecha_nacimiento') or None
            user.empleado.telefono = request.form.get('telefono') or None
            user.empleado.domicilio = request.form.get('domicilio') or None
            user.empleado.observaciones = request.form.get('observaciones') or None
            
            # Solo permitir modificar el área si el usuario es 'Administrador'
            if current_user.rol == 'Administrador':
                area_nombre = request.form.get('area_id')
                area = Area.query.filter_by(nombre=area_nombre).first()
                if area:
                    user.empleado.area_id = area.id
                else:
                    flash('Área no encontrada', 'error')
                    return redirect(url_for('personal.ver_perfil', id=user.id))
            
            # Permitir modificar la contraseña solo si el usuario actual es el dueño del perfil
            if current_user.id == user.id and request.form.get('password'):
                user.set_password(request.form.get('password'))
            
            success, message = user.update()
            if success:
                flash('Perfil actualizado con éxito', 'success')
            else:
                flash(message, 'error')
            return redirect(url_for('personal.ver_perfil', id=user.id))
    
    area = Area.query.filter_by(id=user.empleado.area_id).first()
    saldo_area = area.saldo if area else 'N/A'
    archivos = servicio_personal.conseguir_archivos_de_empleado(user.empleado.id)
    
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
        {'name': 'username', 'label': 'Nombre de Usuario', 'type': 'text', 'value': user.username or ''},
        {'name': 'email', 'label': 'Correo Electrónico', 'type': 'email', 'value': user.empleado.email or ''},
        {'name': 'nombre', 'label': 'Nombre', 'type': 'text', 'value': user.empleado.nombre or ''},
        {'name': 'apellido', 'label': 'Apellido', 'type': 'text', 'value': user.empleado.apellido or ''},
        {'name': 'dni', 'label': 'DNI', 'type': 'text', 'value': user.empleado.dni or ''},
        {'name': 'area_id', 'label': 'Área', 'type': 'select', 'value': user.empleado.area_id or '', 'options': [area.nombre for area in areas], 'disabled': current_user.rol != 'Administrador'},
        {'name': 'dependencia', 'label': 'Dependencia', 'type': 'select', 'value': user.empleado.dependencia or '', 'options': dependencias},
        {'name': 'cargo', 'label': 'Cargo', 'type': 'select', 'value': user.empleado.cargo or '', 'options': cargos},
        {'name': 'subdivision_cargo', 'label': 'Subdivisión del Cargo', 'type': 'select', 'value': user.empleado.subdivision_cargo or '', 'options': subdivisiones_cargo.get(user.empleado.cargo, [])},
        {'name': 'fecha_nacimiento', 'label': 'Fecha de Nacimiento', 'type': 'date', 'value': user.empleado.fecha_nacimiento or ''},
        {'name': 'telefono', 'label': 'Teléfono', 'type': 'text', 'value': user.empleado.telefono or ''},
        {'name': 'domicilio', 'label': 'Domicilio', 'type': 'text', 'value': user.empleado.domicilio or ''},
        {'name': 'observaciones', 'label': 'Observaciones', 'type': 'textarea', 'value': user.empleado.observaciones or ''},
    ]
    
    return render_template('personal/ver_perfil.html', user=user, saldo_area=saldo_area, archivos=archivos, campos=campos)

@personal_bp.route('/archivo/eliminar/<int:id>', methods=['POST'])
@role_required('Administrador', 'Colaborador', 'Personal') 
def eliminar_archivo(id):
    servicio_personal.eliminar_archivo(id)
    flash('Archivo eliminado con éxito', 'success')
    return redirect(url_for('personal.ver_perfil', id=current_user.id))

@personal_bp.route('/archivo/descargar/<int:id>', methods=['GET'])
@role_required('Administrador', 'Colaborador', 'Personal') 
def descargar_archivo(id):
    archivo = Archivo.query.get_or_404(id)    
    return send_file(archivo.filepath, as_attachment=True)

@personal_bp.route('/usuario/inhabilitar/<int:id>', methods=['POST'])
@role_required('Administrador', 'Colaborador') 
def inhabilitar_usuario(id):
    user = User.query.get_or_404(id)
    
    user.habilitado = False
    user.update()
    flash('Usuario inhabilitado con éxito', 'success')
    return redirect(url_for('personal.ver_perfil', id=user.id))

@personal_bp.route('/topicos', methods=['GET'])
@role_required('Administrador', 'Colaborador', 'Personal') 
def seleccionar_topico():
    return render_template('topicos.html')