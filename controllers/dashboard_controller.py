from flask import Blueprint, render_template, request
from app import db
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', methods=['GET'])
def dashboard():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    # CONSULTA DE TOTALES
    query_totales = """
        SELECT
            SUM(CASE WHEN tv.descripcion = 'ACEPTADO' THEN 1 ELSE 0 END) AS total_aceptados,
            SUM(CASE WHEN tv.descripcion = 'RECONCILIADO' THEN 1 ELSE 0 END) AS total_reconciliados
        FROM convertido c
        JOIN tipovalidacion tv ON c.id_validacion = tv.id_validacion
        WHERE 1=1
    """
    params = {}

    if fecha_inicio:
        query_totales += " AND c.fecha_conversion >= :fecha_inicio"
        params['fecha_inicio'] = fecha_inicio

    if fecha_fin:
        query_totales += " AND c.fecha_conversion <= :fecha_fin"
        params['fecha_fin'] = fecha_fin

    totales = db.session.execute(query_totales, params).fetchone()

    # CONSULTA PARA LA GRÁFICA (AGRUPADO POR FECHA)
    query_grafica = """
        SELECT
            c.fecha_conversion,
            SUM(CASE WHEN tv.descripcion = 'ACEPTADO' THEN 1 ELSE 0 END) AS aceptados,
            SUM(CASE WHEN tv.descripcion = 'RECONCILIADO' THEN 1 ELSE 0 END) AS reconciliados
        FROM convertido c
        JOIN tipovalidacion tv ON c.id_validacion = tv.id_validacion
        WHERE 1=1
    """

    if fecha_inicio:
        query_grafica += " AND c.fecha_conversion >= :fecha_inicio"

    if fecha_fin:
        query_grafica += " AND c.fecha_conversion <= :fecha_fin"

    query_grafica += " GROUP BY c.fecha_conversion ORDER BY c.fecha_conversion"

    grafica_result = db.session.execute(query_grafica, params).fetchall()

    fechas = []
    aceptados = []
    reconciliados = []

    for row in grafica_result:
        fechas.append(row.fecha_conversion.strftime('%Y-%m-%d'))
        aceptados.append(row.aceptados)
        reconciliados.append(row.reconciliados)

    chart_data = {
        'fechas': fechas,
        'aceptados': aceptados,
        'reconciliados': reconciliados
    }

    return render_template('dashboard.html',
                           totales=totales,
                           chart_data=chart_data,
                           fecha_inicio=fecha_inicio,
                           fecha_fin=fecha_fin)
