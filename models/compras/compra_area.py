from models.base import db
from datetime import datetime

compra_area = db.Table(
    "compra_area",
    db.metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("compra_id", db.Integer, db.ForeignKey("compras.id")),
    db.Column("area_id", db.Integer, db.ForeignKey("area.id")),
    db.Column("insertado_en", db.DateTime, default=datetime.now),
    db.Column("actualizado_en", db.DateTime, default=datetime.now, onupdate=datetime.now),
    extend_existing=True
)