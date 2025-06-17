from flask import Blueprint, render_template, request, redirect, url_for, send_file
from app import db
from models.convertido import Convertido
from models.tipo_validacion import TipoValidacion
from models.lugar_conversion import LugarConversion
from datetime import datetime
import pandas as pd
from io import BytesIO
from xhtml2pdf import pisa

convertido_bp = Blueprint("convertido", __name__, url_prefix="/convertido")

@convertido_bp.route("/", methods=["GET"])
def index():
    nombre = request.args.get("nombre", "").strip()
    contacto = request.args.get("contacto", "").strip()
    fecha_inicio = request.args.get("fecha_inicio", "").strip()
    fecha_fin = request.args.get("fecha_fin", "").strip()

    query = Convertido.query.join(TipoValidacion)

    if nombre:
        query = query.filter(
            (Convertido.nombres.ilike(f"%{nombre}%")) |
            (Convertido.apellidos.ilike(f"%{nombre}%"))
        )
    if contacto:
        query = query.filter(Convertido.contacto.ilike(f"%{contacto}%"))
    if fecha_inicio:
        fecha_i = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        query = query.filter(Convertido.fecha_conversion >= fecha_i)
    if fecha_fin:
        fecha_f = datetime.strptime(fecha_fin, "%Y-%m-%d")
        query = query.filter(Convertido.fecha_conversion <= fecha_f)

    page = request.args.get("page", 1, type=int)
    per_page = 20
    pagination = query.order_by(Convertido.id.desc()).paginate(page=page, per_page=per_page)
    registros = pagination.items

    return render_template("convertido/list.html", registros=registros, pagination=pagination,
                           nombre=nombre, contacto=contacto, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

@convertido_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    tipo_validaciones = TipoValidacion.query.all()
    lugares_conversion = LugarConversion.query.all()

    if request.method == "POST":
        nombres = request.form['nombres'].strip()
        apellidos = request.form['apellidos'].strip()
        edad = int(request.form['edad'])
        contacto = request.form['contacto'].strip()
        domicilio = request.form['domicilio'].strip()
        invito = request.form['invito'].strip() or 'N/A'
        id_validacion = int(request.form['id_validacion'])
        id_lugar = int(request.form['id_lugar'])

        fecha_conversion = datetime.now().date() if request.form.get("usar_fecha_actual") else datetime.strptime(request.form["fecha_conversion"], "%Y-%m-%d").date()

        nuevo_registro = Convertido(
            nombres=nombres, apellidos=apellidos, edad=edad, contacto=contacto,
            domicilio=domicilio, invito=invito, id_validacion=id_validacion, 
            id_lugar=id_lugar, fecha_conversion=fecha_conversion
        )
        db.session.add(nuevo_registro)
        db.session.commit()
        return redirect(url_for("convertido.index"))

    return render_template("convertido/form.html", registro=None, tipo_validaciones=tipo_validaciones, lugares_conversion=lugares_conversion)

@convertido_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    registro = Convertido.query.get_or_404(id)
    tipo_validaciones = TipoValidacion.query.all()
    lugares_conversion = LugarConversion.query.all()

    if request.method == "POST":
        registro.nombres = request.form["nombres"]
        registro.apellidos = request.form["apellidos"]
        registro.edad = request.form["edad"]
        registro.contacto = request.form["contacto"]
        registro.domicilio = request.form["domicilio"]
        registro.invito = request.form["invito"]
        registro.id_validacion = request.form["id_validacion"]
        registro.id_lugar = request.form["id_lugar"]
        registro.fecha_conversion = datetime.now().date() if request.form.get("usar_fecha_actual") else datetime.strptime(request.form["fecha_conversion"], "%Y-%m-%d").date()

        db.session.commit()
        return redirect(url_for("convertido.index"))

    return render_template("convertido/form.html", registro=registro, tipo_validaciones=tipo_validaciones, lugares_conversion=lugares_conversion)

@convertido_bp.route("/eliminar/<int:id>")
def eliminar(id):
    registro = Convertido.query.get_or_404(id)
    db.session.delete(registro)
    db.session.commit()
    return redirect(url_for("convertido.index"))

@convertido_bp.route("/export_excel")
def export_excel():
    query = Convertido.query.join(TipoValidacion)

    nombre = request.args.get("nombre", "").strip()
    contacto = request.args.get("contacto", "").strip()
    fecha_inicio = request.args.get("fecha_inicio", "").strip()
    fecha_fin = request.args.get("fecha_fin", "").strip()

    if nombre:
        query = query.filter(
            (Convertido.nombres.ilike(f"%{nombre}%")) |
            (Convertido.apellidos.ilike(f"%{nombre}%"))
        )
    if contacto:
        query = query.filter(Convertido.contacto.ilike(f"%{contacto}%"))
    if fecha_inicio:
        fecha_i = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        query = query.filter(Convertido.fecha_conversion >= fecha_i)
    if fecha_fin:
        fecha_f = datetime.strptime(fecha_fin, "%Y-%m-%d")
        query = query.filter(Convertido.fecha_conversion <= fecha_f)

    registros = query.order_by(Convertido.id.desc()).all()

    data = [{
        'Nombres': r.nombres,
        'Apellidos': r.apellidos,
        'Edad': r.edad,
        'Contacto': r.contacto,
        'Domicilio': r.domicilio,
        'Invito': r.invito,
        'Tipo Validación': r.tipo_validacion.descripcion,
        'Fecha Conversión': r.fecha_conversion.strftime("%Y-%m-%d")
    } for r in registros]

    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Convertidos')
    output.seek(0)
    return send_file(output, download_name="convertidos.xlsx", as_attachment=True)

@convertido_bp.route("/export_pdf")
def export_pdf():
    query = Convertido.query.join(TipoValidacion)

    nombre = request.args.get("nombre", "").strip()
    contacto = request.args.get("contacto", "").strip()
    fecha_inicio = request.args.get("fecha_inicio", "").strip()
    fecha_fin = request.args.get("fecha_fin", "").strip()

    if nombre:
        query = query.filter(
            (Convertido.nombres.ilike(f"%{nombre}%")) |
            (Convertido.apellidos.ilike(f"%{nombre}%"))
        )
    if contacto:
        query = query.filter(Convertido.contacto.ilike(f"%{contacto}%"))
    if fecha_inicio:
        fecha_i = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        query = query.filter(Convertido.fecha_conversion >= fecha_i)
    if fecha_fin:
        fecha_f = datetime.strptime(fecha_fin, "%Y-%m-%d")
        query = query.filter(Convertido.fecha_conversion <= fecha_f)

    registros = query.order_by(Convertido.id.desc()).all()

    rendered = render_template("convertido/reporte_pdf.html", registros=registros)
    pdf = BytesIO()
    pisa.CreatePDF(BytesIO(rendered.encode("utf-8")), dest=pdf)
    pdf.seek(0)
    return send_file(pdf, download_name="convertidos.pdf", as_attachment=True)
