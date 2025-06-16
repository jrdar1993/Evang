from app import db
from datetime import datetime

class LugarConversion(db.Model):
    __tablename__ = 'lugarconversion'
    id = db.Column('id_lugar', db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50), nullable=False)
    fecha_sistemas = db.Column(db.DateTime, default=datetime.utcnow)