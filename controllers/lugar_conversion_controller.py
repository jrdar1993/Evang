from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from models.lugar_conversion import LugarConversion

lugar_conversion_bp = Blueprint("lugar_conversion", __name__, url_prefix="/lugar_conversion")

@lugar_conversion_bp.route("/")
def index():
    registros = LugarConversion.query.all()
    return render_template("lugar_conversion/list.html", registros=registros)

@lugar_conversion_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        descripcion = request.form["descripcion"]
        nuevo_registro = LugarConversion(descripcion=descripcion)
        db.session.add(nuevo_registro)
        db.session.commit()
        return redirect(url_for("lugar_conversion.index"))
    return render_template("lugar_conversion/form.html")

@lugar_conversion_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    registro = LugarConversion.query.get_or_404(id)
    if request.method == "POST":
        registro.descripcion = request.form["descripcion"]
        db.session.commit()
        return redirect(url_for("lugar_conversion.index"))
    return render_template("lugar_conversion/form.html", registro=registro)

@lugar_conversion_bp.route("/eliminar/<int:id>")
def eliminar(id):
    registro = LugarConversion.query.get_or_404(id)
    db.session.delete(registro)
    db.session.commit()
    return redirect(url_for("lugar_conversion.index"))