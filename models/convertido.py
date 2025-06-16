from app import db
from datetime import datetime

class Convertido(db.Model):
    __tablename__ = 'convertido'
    id = db.Column('id_convertido', db.Integer, primary_key=True)
    nombres = db.Column(db.String(25), nullable=False)
    apellidos = db.Column(db.String(25), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    contacto = db.Column(db.String(25), nullable=False)
    domicilio = db.Column(db.String(100))
    invito = db.Column(db.String(25), nullable=False)
    id_validacion = db.Column(db.Integer, db.ForeignKey('tipovalidacion.id_validacion'), nullable=False)
    id_lugar = db.Column(db.Integer, db.ForeignKey('lugarconversion.id_lugar'), nullable=False)
    fecha_conversion = db.Column(db.Date, nullable=False)
    fecha_sistemas = db.Column(db.DateTime, default=datetime.utcnow)