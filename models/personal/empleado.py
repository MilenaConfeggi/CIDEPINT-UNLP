from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import validates
from datetime import datetime
from models.usuarios.usuario import Usuario
from models.usuarios.rol import Rol
from models.usuarios.rol_permiso import RolPermiso
from models.usuarios.permiso import Permiso


from models.compras.compra_empleado import compra_empleado
from models.base import db

class Empleado(db.Model):
    __tablename__ = 'empleado'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='empleado')

    # Las dejo comentadas porque nos rompe el sistema del lado de administracion, por favor, antes de descomentarlas avisennos para que podamos arreglarlo
    usuario_servicio_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True) 
    usuario_servicio = db.relationship('Usuario', back_populates='empleado', uselist=False)

    email = db.Column(db.String(120), unique=True, nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    area = db.relationship('Area', backref=db.backref('empleados', lazy=True))
    dni = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    dependencia = db.Column(db.String(50), nullable=True)
    cargo = db.Column(db.String(50), nullable=True)
    subdivision_cargo = db.Column(db.String(50), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    domicilio = db.Column(db.String(200), nullable=True)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    saldo = db.Column(db.DECIMAL(12,2), default=0.00)   
    observaciones = db.Column(db.Text, nullable=True)
    archivos = db.relationship('Archivo', back_populates='empleado')
    ausencias = db.relationship('Ausencia', back_populates='empleado')
    distribuciones_asociadas = db.relationship(
        "Empleado_Distribucion", back_populates="empleado"
    ) 
    compras = db.relationship('Compra', secondary=compra_empleado ,back_populates='empleados')
    solicitudes = db.relationship('Compra', back_populates='solicitante', cascade='all, delete-orphan')

    @validates('area_id')
    def validate_area(self, key, value):
        if not value:
            raise ValueError("El área no puede estar vacía.")
        return value

    @validates('dependencia')
    def validate_dependencia(self, key, value):
        allowed_dependencias = ['UNLP', 'CIC', 'CONICET']
        if value and value not in allowed_dependencias:
            raise ValueError(f"Dependencia '{value}' no es válida. Debe ser una de {allowed_dependencias}.")
        return value

    @validates('cargo')
    def validate_cargo(self, key, value):
        allowed_cargos = ['Investigador', 'CPA', 'Administrativo', 'Técnico', 'Becario']
        if value and value not in allowed_cargos:
            raise ValueError(f"Cargo '{value}' no es válido. Debe ser uno de {allowed_cargos}.")
        return value

    @validates('subdivision_cargo')
    def validate_subdivision_cargo(self, key, value):
        allowed_subdivisiones = {
            'Investigador': ['Asistente', 'Adjunto', 'Independiente', 'Principal', 'Superior'],
            'CPA': ['Profesional Principal', 'Profesional Adjunto', 'Profesional Asistente','Técnico Principal', 'Técnico Asociado', 'Técnico Asistente','Técnico Auxiliar','Otro'],
            'Técnico': ['Otro'],
            'Administrativo': ['ART 9', 'Ley 10430', 'Otro'],
            'Becario' : ['De entrenamiento','Doctoral','Posdoctoral', 'Otro']
        }
        if self.cargo and (self.cargo not in allowed_subdivisiones or value not in allowed_subdivisiones[self.cargo]):
            raise ValueError(f"Subdivisión de cargo '{value}' no es válida para el cargo '{self.cargo}'.")
        return value

    def __init__(self, user, email, area, dni, nombre, apellido, dependencia=None, cargo=None, subdivision_cargo=None, telefono=None, domicilio=None, fecha_nacimiento=None, observaciones=None, habilitado=True, rol='Personal', saldo=0.00):
        self.user = user
        self.email = email
        self.area = area
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.dependencia = dependencia
        self.cargo = cargo
        self.subdivision_cargo = subdivision_cargo
        self.telefono = telefono
        self.domicilio = domicilio
        self.fecha_nacimiento = fecha_nacimiento
        self.observaciones = observaciones
        self.habilitado = habilitado
        self.rol = rol
        self.primer_login = True
        self.usuario_servicio = None
        self.saldo = saldo

    def __repr__(self) -> str:
        return f"Empleado {self.nombre} {self.apellido}"

    def save(self) -> tuple:
        try:
            db.session.add(self)
            db.session.commit()
            return True, "Empleado creado con éxito"
        except IntegrityError:
            db.session.rollback()
            return False, "El email o DNI ya existe."
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error en la base de datos: {str(e)}"

    def update(self) -> tuple:
        try:
            db.session.commit()
            return True, "Empleado actualizado con éxito"
        except IntegrityError:
            db.session.rollback()
            return False, "El email o DNI ya existe."
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error en la base de datos: {str(e)}"

    def delete(self) -> tuple:
        try:
            db.session.delete(self)
            db.session.commit()
            return True, "Empleado eliminado con éxito"
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error en la base de datos: {str(e)}"