from app import db
from datetime import datetime

class TipoValidacion(db.Model):
    __tablename__ = 'tipovalidacion'
    id = db.Column('id_validacion', db.Integer, primary_key=True)
    descripcion = db.Column(db.String(25), nullable=False)
    fecha_sistemas = db.Column(db.DateTime, default=datetime.utcnow)