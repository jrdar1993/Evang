from flask import Blueprint, render_template
from app import db
from models.convertido import Convertido
from models.tipo_validacion import TipoValidacion

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def dashboard():
    # Consulta SQL usando SQLAlchemy puro
    resultado = db.session.execute("""
        SELECT
            SUM(CASE WHEN tv.descripcion = 'ACEPTADO' THEN 1 ELSE 0 END) AS total_aceptados,
            SUM(CASE WHEN tv.descripcion = 'RECONCILIADO' THEN 1 ELSE 0 END) AS total_reconciliados
        FROM convertido c
        JOIN tipovalidacion tv ON c.id_validacion = tv.id_validacion
    """).fetchone()

    return render_template('dashboard.html', datos=resultado)
