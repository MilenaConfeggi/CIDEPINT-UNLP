from models.base import db
from datetime import datetime

compra_fondo = db.Table(
    "compra_fondo",
    db.metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("compra_id", db.Integer, db.ForeignKey("compras.id")),
    db.Column("fondo_id", db.Integer, db.ForeignKey("fondo.id")), 
    db.Column("contribucion", db.DECIMAL(12,2), nullable=False),
    db.Column("insertado_en", db.DateTime, default=datetime.now),
    db.Column("actualizado_en", db.DateTime, default=datetime.now, onupdate=datetime.now),
    extend_existing=True
)