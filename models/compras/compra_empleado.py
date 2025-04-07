from models.base import db
from datetime import datetime

compra_empleado = db.Table(
    "compra_empleado",
    db.metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("compra_id", db.Integer, db.ForeignKey("compras.id")),
    db.Column("empleado_id", db.Integer, db.ForeignKey("empleado.id")),
    db.Column("contribucion", db.DECIMAL(12,2), nullable=False),
    db.Column("insertado_en", db.DateTime, default=datetime.now),
    db.Column("actualizado_en", db.DateTime, default=datetime.now, onupdate=datetime.now),
    extend_existing=True
)