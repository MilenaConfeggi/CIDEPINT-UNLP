from models.base import db
from models.distribucion.distribucion import Distribucion
from models.personal.empleado import Empleado
from models.empleado_distribucion.empleado_distribucion import Empleado_Distribucion
from datetime import datetime

def seed_distribuciones():
    # Crear distribuciones
    distribuciones_data = [
        {
            'porcentaje_area': 40.0,
            'porcentaje_empleados': 50.0,
            'porcentaje_comisiones': 19.0,
            'monto_a_distribuir': 1000.0,
            'costos': 200.0,
            'legajo_id': 16837,  # Asignar un legajo existente
            'ganancias_de_id': 1,  # Asignar un área existente
            'costos_de_id': 1,  # Asignar un área existente
        },
        {
            'porcentaje_area': 30.0,
            'porcentaje_empleados': 60.0,
            'porcentaje_comisiones': 10.0,
            'monto_a_distribuir': 2000.0,
            'costos': 300.0,
            'legajo_id': 16838,  # Asignar un legajo existente
            'ganancias_de_id': 2,  # Asignar un área existente
            'costos_de_id': 2,  # Asignar un área existente
        }
    ]

    for data in distribuciones_data:
        distribucion = Distribucion(
            porcentaje_area=data['porcentaje_area'],
            porcentaje_empleados=data['porcentaje_empleados'],
            porcentaje_comisiones=data['porcentaje_comisiones'],
            monto_a_distribuir=data['monto_a_distribuir'],
            costos=data['costos'],
            legajo_id=data['legajo_id'],
            ganancias_de_id=data['ganancias_de_id'],
            costos_de_id=data['costos_de_id']
        )
        db.session.add(distribucion)
        db.session.commit()

        # Asignar empleados a la distribucion
        empleados = Empleado.query.all()
        for empleado in empleados:
            empleado_distribucion = Empleado_Distribucion(
                distribucion_id=distribucion.id,
                empleado_id=empleado.id
            )
            db.session.add(empleado_distribucion)
        db.session.commit()
