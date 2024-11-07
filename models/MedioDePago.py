from sqlalchemy import Column, Integer, String
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.base import db

class MedioPago(db.Model):
    __tablename__ = 'medio_de_pago'
    id = db.Column(db.Integer, primary_key=True)
    medio_de_pago = db.Column(db.String(100), nullable=False)