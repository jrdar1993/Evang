from flask import Blueprint, render_template, request
from app import db
from models.convertido import Convertido
from models.tipo_validacion import TipoValidacion

from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', methods=['GET', 'POST'])
def dashboard():
    # Capturamos fechas del formulario
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    query = """
        SELECT
            SUM(CASE WHEN tv.descripcion = 'ACEPTADO' THEN 1 ELSE 0 END) AS total_aceptados,
            SUM(CASE WHEN tv.descripcion = 'RECONCILIADO' THEN 1 ELSE 0 END) AS total_reconciliados
        FROM convertido c
        JOIN tipovalidacion tv ON c.id_validacion = tv.id_validacion
        WHERE 1=1
    """

    params = {}

    # Si hay filtros de fecha, los agregamos
    if fecha_inicio:
        query += " AND c.fecha_conversion >= :fecha_inicio"
        params['fecha_inicio'] = fecha_inicio

    if fecha_fin:
        query += " AND c.fecha_conversion <= :fecha_fin"
        params['fecha_fin'] = fecha_fin

    resultado = db.session.execute(query, params).fetchone()

    return render_template('dashboard.html', datos=resultado, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
