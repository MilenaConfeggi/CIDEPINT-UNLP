from flask import flash, redirect, render_template, request, url_for, Blueprint, session
from models.personal.area import Area
from models.personal.personal import User

from administracion.src.web.controllers.roles import role_required  # Importa el decorador

area_bp = Blueprint("area", __name__, url_prefix="/area")

@area_bp.route('/listar', methods=['GET'])
@role_required('Administrador', 'Colaborador')
def listar_areas():
    areas = Area.query.all()
    return render_template('personal/listar_areas.html', areas=areas)

@area_bp.route('/crear', methods=['GET', 'POST'])
@role_required('Administrador', 'Colaborador')
def crear_area():
    if request.method == 'POST':
        nombre = request.form['nombre']
        saldo = request.form['saldo']
        
        nueva_area = Area(nombre=nombre, saldo=saldo)
        success, message = nueva_area.save()
        
        if success:
            flash('Área creada con éxito', 'success')
        else:
            flash(message, 'error')    
            
    return render_template('personal/crear_area.html')

@area_bp.route('/modificar/<int:id>', methods=['GET', 'POST'])
@role_required('Administrador', 'Colaborador')
def modificar_area(id):
    area = Area.query.get_or_404(id)
    
    if request.method == 'POST':
        area.nombre = request.form['nombre']
        area.saldo = request.form['saldo']
        
        success, message = area.update()
        if success:
            flash('Área actualizada con éxito', 'success')
        else:
            flash(message, 'error')    
    return render_template('personal/modificar_area.html', area=area)

@area_bp.route('/eliminar/<int:id>', methods=['POST'])
@role_required('Administrador', 'Colaborador')
def eliminar_area(id):
    area = Area.query.get_or_404(id)
    
    # Verificar si hay usuarios asociados a esta área
    usuarios_asociados = User.query.filter_by(area_id=id).count()
    if usuarios_asociados > 0:
        flash('No se puede eliminar el área porque hay usuarios asociados a ella.', 'error')    
    success, message = area.delete()
    if success:
        return redirect(url_for('area.listar_areas'))
    else:
        flash(message, 'error')
    
   