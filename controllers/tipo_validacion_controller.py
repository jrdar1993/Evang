from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from models.tipo_validacion import TipoValidacion

tipo_validacion_bp = Blueprint("tipo_validacion", __name__, url_prefix="/tipo_validacion")

@tipo_validacion_bp.route("/")
def index():
    registros = TipoValidacion.query.all()
    return render_template("tipo_validacion/list.html", registros=registros)

@tipo_validacion_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        descripcion = request.form["descripcion"]
        nuevo_registro = TipoValidacion(descripcion=descripcion)
        db.session.add(nuevo_registro)
        db.session.commit()
        return redirect(url_for("tipo_validacion.index"))
    return render_template("tipo_validacion/form.html")

@tipo_validacion_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    registro = TipoValidacion.query.get_or_404(id)
    if request.method == "POST":
        registro.descripcion = request.form["descripcion"]
        db.session.commit()
        return redirect(url_for("tipo_validacion.index"))
    return render_template("tipo_validacion/form.html", registro=registro)

@tipo_validacion_bp.route("/eliminar/<int:id>")
def eliminar(id):
    registro = TipoValidacion.query.get_or_404(id)
    db.session.delete(registro)
    db.session.commit()
    return redirect(url_for("tipo_validacion.index"))